import json
import uuid
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings
from app.db.session import get_db
from app.models.base import Base

# Disable email sending in tests regardless of .env — use a fake SMTP host
# so checks like "if not settings.SMTP_HOST" still pass but no real email is sent.
settings.SMTP_HOST = "localhost"


sa.event.listen(sa.Engine, "connect", lambda c, _: c.execute("PRAGMA journal_mode=WAL") or c.execute("PRAGMA foreign_keys=ON"))


from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB, TIMESTAMP as PG_TIMESTAMP
from sqlalchemy.ext.compiler import compiles


@compiles(PG_UUID, "sqlite")
@compiles(PG_UUID, "default")
def compile_uuid(type_, compiler, **kw):
    return "VARCHAR(36)"


# Fix PG_UUID processing for SQLite — accepts both uuid.UUID objects and strings
_orig_uuid_bind = PG_UUID.bind_processor
_orig_uuid_result = PG_UUID.result_processor

def _uuid_bind_processor(self, dialect):
    if dialect.name == "sqlite":
        def process(value):
            if value is not None:
                return str(value)
            return value
        return process
    return _orig_uuid_bind(self, dialect) if _orig_uuid_bind else None

def _uuid_result_processor(self, dialect, coltype):
    if dialect.name == "sqlite":
        def process(value):
            if value is not None:
                return uuid.UUID(value) if isinstance(value, str) else value
            return value
        return process
    return _orig_uuid_result(self, dialect, coltype) if _orig_uuid_result else None

PG_UUID.bind_processor = _uuid_bind_processor
PG_UUID.result_processor = _uuid_result_processor


# Fix JSONB processing for SQLite — serialize/deserialize JSON
_orig_jsonb_bind = PG_JSONB.bind_processor
_orig_jsonb_result = PG_JSONB.result_processor

def _jsonb_bind_processor(self, dialect):
    if dialect.name == "sqlite":
        def process(value):
            if value is not None:
                return json.dumps(value)
            return value
        return process
    return _orig_jsonb_bind(self, dialect) if _orig_jsonb_bind else None

def _jsonb_result_processor(self, dialect, coltype):
    if dialect.name == "sqlite":
        def process(value):
            if value is not None:
                return json.loads(value)
            return value
        return process
    return _orig_jsonb_result(self, dialect, coltype) if _orig_jsonb_result else None

PG_JSONB.bind_processor = _jsonb_bind_processor
PG_JSONB.result_processor = _jsonb_result_processor


@compiles(PG_JSONB, "sqlite")
@compiles(PG_JSONB, "default")
def compile_jsonb(type_, compiler, **kw):
    return "TEXT"


@compiles(PG_TIMESTAMP, "sqlite")
@compiles(PG_TIMESTAMP, "default")
def compile_timestamp(type_, compiler, **kw):
    return "TIMESTAMP"


engine = sa.create_engine(
    "sqlite:///file::memory:?cache=shared&mode=memory&uri=true",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "country": "US",
        "city": "New York",
    }


@pytest.fixture
def registered_user(client, user_data):
    resp = client.post("/api/auth/register", json=user_data)
    assert resp.status_code == 201, resp.text
    return resp.json()


@pytest.fixture
def user_token(client, user_data, registered_user):
    resp = client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"],
    })
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.fixture
def auth_header(user_token):
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def user_id(registered_user):
    return registered_user["id"]


@pytest.fixture
def project_data():
    return {"name": "Test Project", "description": "A project for testing"}


@pytest.fixture
def user_project(client, auth_header, project_data):
    resp = client.post("/api/projects", json=project_data, headers=auth_header)
    assert resp.status_code == 201, resp.text
    return resp.json()


@pytest.fixture
def project_id(user_project):
    return user_project["id"]


@pytest.fixture
def note_data(project_id):
    return {
        "project_id": project_id,
        "title": "Test Note",
        "content": "<p>Hello world</p>",
        "note_type": "documentation",
    }


@pytest.fixture
def task_data(project_id):
    return {
        "project_id": project_id,
        "title": "Test Task",
        "description": "A task for testing",
        "status": "todo",
        "priority": "medium",
    }


@pytest.fixture
def admin_setup(client, db):
    """Register a user and promote to admin. Returns (token, headers_dict)."""
    email = "admin@example.com"
    password = "AdminPass123!"
    client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "first_name": "Admin",
        "last_name": "User",
        "country": "US",
        "city": "NYC",
    })
    from app.models.user import User
    admin_user = db.query(User).filter(User.email == email).first()
    admin_user.role = "admin"
    db.commit()
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return token, {"Authorization": f"Bearer {token}"}
