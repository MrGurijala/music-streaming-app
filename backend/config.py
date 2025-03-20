import boto3

def get_ssm_parameter(name: str) -> str:
    """Fetches parameter securely from AWS SSM Parameter Store."""
    client = boto3.client("ssm", region_name="eu-west-2")
    response = client.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]

class Settings:
    DATABASE_URL: str = get_ssm_parameter("/music-streaming-app/DATABASE_URL")
    AWS_ACCESS_KEY_ID: str = get_ssm_parameter("/music-streaming-app/AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = get_ssm_parameter("/music-streaming-app/AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = "eu-west-2"  # Usually static, can be stored in SSM if needed
    S3_TRANSCODED_BUCKET_NAME: str = get_ssm_parameter("/music-streaming-app/S3_TRANSCODED_BUCKET_NAME")
    JWT_SECRET_KEY: str = get_ssm_parameter("/music-streaming-app/JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60

settings = Settings()
