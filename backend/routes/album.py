from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.services.db import get_db
from backend.models import Album, AlbumSong
from backend.schemas.song import AddSongRequest

albums_router = APIRouter()

# Create a new album
@albums_router.post("/create")
def create_album(name: str, artist: str, db: Session = Depends(get_db)):
    album = Album(name=name, artist=artist)
    db.add(album)
    db.commit()
    db.refresh(album)
    return {"message": "Album created successfully", "album": album}

# Get all albums
@albums_router.get("/")
def get_albums(limit: int = Query(10, description="Number of albums to return"), db: Session = Depends(get_db)):
    albums = db.query(Album).limit(limit).all()
    return albums

# Get album details
@albums_router.get("/{album_id}")
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

# Add a song to an album
@albums_router.post("/{album_id}/songs}")
def add_song_to_album(album_id: int, song: AddSongRequest, db: Session = Depends(get_db)):
    album_song = AlbumSong(album_id=album_id, song_id=song.song_id)
    db.add(album_song)
    db.commit()
    return {"message": "Song added to album"}

# Remove a song from an album
@albums_router.delete("/{album_id}/songs/{song_id}")
def remove_song_from_album(album_id: int, song_id: int, db: Session = Depends(get_db)):
    album_song = db.query(AlbumSong).filter_by(album_id=album_id, song_id=song_id).first()
    if not album_song:
        raise HTTPException(status_code=404, detail="Song not found in album")
    db.delete(album_song)
    db.commit()
    return {"message": "Song removed from album"}

# Delete an album
@albums_router.delete("/{album_id}")
def delete_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    db.delete(album)
    db.commit()
    return {"message": "Album deleted successfully"}
