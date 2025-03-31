from fastapi import FastAPI, Request
import uvicorn
import time
#from mangum import Mangum 
from backend.routes.auth import auth_router
from backend.routes.album import albums_router
from backend.routes.favourite import favorites_router
from backend.routes.playlist import playlists_router
from backend.routes.songs import songs_router


# Initialize FastAPI app
app = FastAPI()

@app.middleware("http")
async def log_request_duration(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    print(f"{request.method} {request.url.path} took {duration:.2f}ms")
    return response

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(albums_router, prefix="/albums", tags=["Albums"])
app.include_router(favorites_router, prefix="/favorites", tags=["Favorites"])
app.include_router(playlists_router, prefix="/playlists", tags=["Playlists"])
app.include_router(songs_router, prefix="/songs", tags=["Songs"])

# API Documentation
@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/docs")
def get_docs():
    return {"message": "Visit /docs for Swagger UI"}


# Lambda handler for AWS Lambda deployment
#handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
