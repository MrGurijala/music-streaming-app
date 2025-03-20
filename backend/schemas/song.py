from pydantic import BaseModel

class AddSongRequest(BaseModel):
    song_id: int

class AddUserRequest(BaseModel):
    user_id: int
