from fastapi import FastAPI
import uvicorn
from routes.auth import auth_router

# Initialize FastAPI app
app = FastAPI()

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# API Documentation
@app.get("/docs")
def get_docs():
    return {"message": "Visit /docs for Swagger UI"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
