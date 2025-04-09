import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Internal cache
_cached_url = None
_engine = None
_SessionLocal = None

def get_database_url():
    print("📦 Fetching DATABASE_URL from SSM")
    ssm = boto3.client("ssm", region_name="eu-west-2")
    print("Before Got database URL")
    #param = ssm.get_parameter(Name="/music-streaming-app/DATABASE_URL", WithDecryption=True)
    print ("param:, param")
    print("✅ Got database URL")
    #return param["Parameter"]["Value"]
    return "postgresql://admingrv:Haharams1@music-stream-db.c1amswi2whm3.eu-west-2.rds.amazonaws.com:5432/music_stream_db"
def get_db():
    global _cached_url, _engine, _SessionLocal

    if _SessionLocal is None:
        _cached_url = get_database_url()
        _engine = create_engine(
            _cached_url,
            echo=False,
            pool_size=10,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800
        )
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
