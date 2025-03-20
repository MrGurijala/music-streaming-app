import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Function to fetch DATABASE_URL from AWS SSM Parameter Store
def get_database_url():
    ssm_client = boto3.client("ssm", region_name="eu-west-2")  # Change to your AWS region
    response = ssm_client.get_parameter(Name="/music-streaming-app/DATABASE_URL", WithDecryption=True)
    return response["Parameter"]["Value"]

# Fetch DATABASE_URL from AWS SSM
DATABASE_URL = get_database_url()

# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for defining tables
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
