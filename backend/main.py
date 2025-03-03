from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import auth, songs, upload

# Initialize FastAPI app
app = FastAPI(title="Music Streaming API", version="1.0")

# Enable CORS (Cross-Origin Resource Sharing) for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
#app.include_router(upload_router, prefix="/api/v1")
#app.include_router(stream_router, prefix="/api/v1")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(songs.router, prefix="/songs", tags=["Songs"])


# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Music Streaming API!"}

# Run the FastAPI server when executing this file directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
