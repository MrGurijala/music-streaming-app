from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.db import get_db
from models import User
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
from services.auth import create_access_token, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()

# User Signup
@auth_router.post("/signup")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully", "user_id": user.id}

# User Login
@auth_router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# Get Current User
@auth_router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = create_access_token.decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user.username, "email": user.email}
