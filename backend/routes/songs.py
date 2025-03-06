from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from services.db import get_db
from models import Song
from services.aws_service import get_transcoded_file_url

songs_router = APIRouter()

# Add a new song
@songs_router.post("/")
def add_song(title: str, artist: str, album: str, url: str, cache: bool = False, db: Session = Depends(get_db)):
    song = Song(title=title, artist=artist, album=album, url=url)
    db.add(song)
    db.commit()
    db.refresh(song)
    return {"message": "Song added successfully", "song": song}

# Get all songs with limit
@songs_router.get("/")
def get_songs(limit: int = Query(10, description="Number of songs to return"), db: Session = Depends(get_db)):
    songs = db.query(Song).limit(limit).all()
    return songs

# Get a specific song
@songs_router.get("/{song_id}")
def get_song(song_id: int, db: Session = Depends(get_db)):    
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    song_data = {"id": song.id, "title": song.title, "artist": song.artist, "album": song.album, "url": song.url}
    return song_data

# Search songs
@songs_router.get("/search")
def search_songs(query: str, db: Session = Depends(get_db)):
    songs = db.query(Song).filter(Song.title.ilike(f"%{query}%") | Song.artist.ilike(f"%{query}%") | Song.album.ilike(f"%{query}%")).all()
    return songs

# Stream song using S3 pre-signed URL
@songs_router.get("/stream/{song_id}")
def stream_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    presigned_url = get_transcoded_file_url(song.url)
    return {"stream_url": presigned_url}