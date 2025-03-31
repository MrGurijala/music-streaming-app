from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.services.db import get_db
from backend.models import Favorite
from backend.schemas.song import AddSongRequest

favorites_router = APIRouter()

# Add a song to favorites
@favorites_router.post("/add_favorite/{user_id}")
def add_favorite(user_id: int, song: AddSongRequest, db: Session = Depends(get_db)):
    favorite = Favorite(user_id=user_id, song_id=song.song_id)
    db.add(favorite)
    db.commit()
    return {"message": "Song added to favorites"}

# Get all favorite songs for a user
@favorites_router.get("/{user_id}")
def get_favorites(user_id: int, db: Session = Depends(get_db)):
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    return favorites

# Remove a song from favorites
@favorites_router.delete("/{user_id}/{song_id}")
def remove_favorite(user_id: int, song_id: int, db: Session = Depends(get_db)):
    favorite = db.query(Favorite).filter_by(user_id=user_id, song_id=song_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Song not found in favorites")
    db.delete(favorite)
    db.commit()
    return {"message": "Song removed from favorites"}
