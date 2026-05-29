import io
import typing
from urllib.parse import urljoin

import boto3
import json
from botocore.exceptions import ClientError

from app.core.config import settings


def _get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT_URL,
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
        use_ssl=(settings.S3_USE_SSL.lower() == "true") if isinstance(settings.S3_USE_SSL, str) else bool(settings.S3_USE_SSL),
    )

def ensure_bucket_exists(bucket_name: str) -> None:
    client = _get_s3_client()
    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError:
        client.create_bucket(Bucket=bucket_name)


def upload_fileobj(fileobj: typing.BinaryIO, key: str, content_type: str | None = None) -> str:
    bucket = settings.S3_BUCKET_NAME
    client = _get_s3_client()
    ensure_bucket_exists(bucket)
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    # Upload
    client.upload_fileobj(fileobj, bucket, key, ExtraArgs=extra_args or None)

    # Return S3 object key (not a public URL). Clients should request
    # presigned URLs when they need temporary access.
    return key


def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """Generate a presigned GET URL for the given object key."""
    client = _get_s3_client()
    bucket = settings.S3_BUCKET_NAME
    try:
        url = client.generate_presigned_url(
            "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in
        )
        return url
    except ClientError:
        raise


def delete_object(key: str) -> None:
    """Delete an object from the configured bucket. Swallow errors."""
    bucket = settings.S3_BUCKET_NAME
    client = _get_s3_client()
    try:
        client.delete_object(Bucket=bucket, Key=key)
    except ClientError:
        # best-effort delete; ignore failures
        return
