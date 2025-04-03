from fastapi import FastAPI
from mangum import Mangum
from routes.auth import auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

handler = Mangum(app)
