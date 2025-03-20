import boto3
import os

AWS_REGION = "eu-west-2"
S3_RAW_BUCKET = "music-raw-bucket"
S3_TRANSCODED_BUCKET = "music-transcoded-bucket"

# Initialize S3 client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def upload_file_to_s3(file_name, file_obj):
    """Uploads a raw file to S3 (music-raw-bucket)"""
    try:
        s3.upload_fileobj(file_obj, S3_RAW_BUCKET, file_name)
        return f"https://{S3_RAW_BUCKET}.s3.amazonaws.com/{file_name}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def get_transcoded_file_url(file_name, expiration=3600):
    """Generates a signed URL for accessing transcoded files"""
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_TRANSCODED_BUCKET, "Key": file_name},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return None
