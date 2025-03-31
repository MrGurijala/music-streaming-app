from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.services.db import get_db
from backend.models import Playlist, PlaylistSong
from backend.schemas.song import AddUserRequest, AddSongRequest

playlists_router = APIRouter()

# Create a new playlist
@playlists_router.post("/")
def create_playlist(name: str, user: AddUserRequest, db: Session = Depends(get_db)):
    playlist = Playlist(name=name, user_id=user.user_id)
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return {"message": "Playlist created successfully", "playlist": playlist}

# Get all playlists for a user
@playlists_router.get("/user/{user_id}")
def get_playlists(user_id: int, db: Session = Depends(get_db)):
    playlists = db.query(Playlist).filter(Playlist.user_id == user_id).all()
    return playlists

# Add a song to a playlist
@playlists_router.post("/{playlist_id}/songs")
def add_song_to_playlist(playlist_id: int, song: AddSongRequest, db: Session = Depends(get_db)):
    playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song.song_id)
    db.add(playlist_song)
    db.commit()
    return {"message": "Song added to playlist"}

# Remove a song from a playlist
@playlists_router.delete("/{playlist_id}/songs/{song_id}")
def remove_song_from_playlist(playlist_id: int, song_id: int, db: Session = Depends(get_db)):
    playlist_song = db.query(PlaylistSong).filter_by(playlist_id=playlist_id, song_id=song_id).first()
    if not playlist_song:
        raise HTTPException(status_code=404, detail="Song not found in playlist")
    db.delete(playlist_song)
    db.commit()
    return {"message": "Song removed from playlist"}

# Delete a playlist
@playlists_router.delete("/{playlist_id}")
def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted successfully"}