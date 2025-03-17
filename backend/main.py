from fastapi import FastAPI
import uvicorn
from mangum import Mangum 
from routes.auth import auth_router
from routes.album import albums_router
from routes.favourite import favorites_router
from routes.playlist import playlists_router
from routes.songs import songs_router

# Initialize FastAPI app
app = FastAPI()

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(albums_router, prefix="/albums", tags=["Albums"])
app.include_router(favorites_router, prefix="/favorites", tags=["Favorites"])
app.include_router(playlists_router, prefix="/playlists", tags=["Playlists"])
app.include_router(songs_router, prefix="/songs", tags=["Songs"])

# API Documentation
@app.get("/docs")
def get_docs():
    return {"message": "Visit /docs for Swagger UI"}

# Lambda handler for AWS Lambda deployment
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
