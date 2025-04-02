from fastapi import FastAPI
from mangum import Mangum
from routes.songs import songs_router

app = FastAPI()
app.include_router(songs_router, prefix="/songs", tags=["Songs"])

handler = Mangum(app)
