# Build stage
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --gid 1001 app
COPY --from=builder /install /usr/local
COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic
RUN mkdir -p /app/logs && chown -R app:app /app
USER app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import http.client; c=http.client.HTTPConnection('localhost',8000); c.request('GET','/health'); r=c.getresponse(); exit(0) if r.status==200 else exit(1)"
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
