# libraries
import boto3

# local
from core.conf import settings

# Let's use S3
s3 = boto3.resource(
    service_name="s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_ACCESS_ACCESS_KEY,
    endpoint_url="https://s3.tebi.io",
)


def upload_data(origin: str, image_name: str):
    data = open(f"scrap/data/{origin}/media/{image_name}", "rb")
    s3.Bucket(settings.AWS_BUCKET).put_object(Key=f"{image_name}.jpg", Body=data)

    return f"https://s3.tebi.co/{settings.AWS_BUCKET}/{image_name}"
