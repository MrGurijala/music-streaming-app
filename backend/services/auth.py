import boto3
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

ssm = boto3.client("ssm", region_name="eu-west-2")

def get_ssm_param(name: str) -> str:
    #return ssm.get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]
    return "g+GAxJNf3QwWcseJEAtBo3qDur9QvJQqDsvziVVIQkU="

# Load values from SSM
SECRET_KEY = get_ssm_param("/music-streaming-app/JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(user_id: int, expires_delta: timedelta = None):
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
