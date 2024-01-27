# default
import uuid

# libraries
import boto3

# local
from core.conf import settings, is_dev_env

# Let's use S3
s3 = boto3.resource(
    service_name="s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_ACCESS_ACCESS_KEY,
    endpoint_url="https://s3.tebi.io",
)
bucket = s3.Bucket(settings.AWS_BUCKET)


def upload_image(image_name: str):
    uid = str(uuid.uuid4())[:8]
    data = open(f"scrap/data/media/{image_name}", "rb")
    object_id = f"{uid}_{image_name}"
    bucket.put_object(Key=object_id, Body=data)

    return (
        f"https://s3.tebi.io/{settings.AWS_BUCKET}/{object_id}"
        if is_dev_env
        else f"https://files.betterme.news/{object_id}"
    )


def delete_image(image_link: str):
    object_key = image_link.split("/")[-1]
    s3.Object(settings.AWS_BUCKET, object_key).delete()
