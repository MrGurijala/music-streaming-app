import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from models import Base  # Import your SQLAlchemy models
from models import Base
from backend.services.db import engine

# Fetch DATABASE_URL from environment variables or SSM
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admingrv:Haharams1@music-stream-db.c1amswi2whm3.eu-west-2.rds.amazonaws.com:5432/music_stream_db")

#DATABASE_URL = "postgresql://grv:yourpassword@localhost/musicstream_local"

# Create engine
engine = create_engine(DATABASE_URL)

# Create tables
def create_tables():
    print("Creating tables in AWS RDS PostgreSQL...")
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()