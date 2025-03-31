import random
import os
import argparse
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Base, User, Song, Album, AlbumSong, Playlist, PlaylistSong, Favorite

# ✅ Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admingrv:Haharams1@music-stream-db.c1amswi2whm3.eu-west-2.rds.amazonaws.com:5432/music_stream_db")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# ✅ Initialize Faker
fake = Faker()

# ✅ Session to interact with DB
def get_session():
    return Session(bind=engine)

# ✅ Create Users
def create_users(session, num_users=2500):
    faker = Faker()
    existing_usernames = set()
    existing_emails = set()
    
    users = []
    
    while len(users) < num_users:
        username = faker.user_name()
        email = faker.email()
        
        # Ensure unique username and email
        if username not in existing_usernames and email not in existing_emails:
            password_hash = faker.password()
            user = User(username=username, email=email, password_hash=password_hash)
            users.append(user)
            existing_usernames.add(username)
            existing_emails.add(email)

    session.add_all(users)
    session.commit()


# ✅ Create Songs (From S3 Bucket)
def create_songs(session):
    genres = ["classical", "electronic", "pop", "rock"]
    base_url = "s3://music-transcoded-bucket/songs/"
    
    for genre in genres:
        for i in range(1, 101):  # Song files from 1.mp3 to 100.mp3
            song = Song(
                title=f"{genre.capitalize()} Song {i}",
                artist=fake.name(),
                album=f"{genre.capitalize()} Album {random.randint(1, 500)}",
                url=f"{base_url}{genre}/{genre}/{i}.mp3"
            )
            session.add(song)
    
    session.commit()
    print("✅ Created 400 songs from S3.")

# ✅ Create Albums with Songs
def create_albums_with_songs(session, album_count=10000, songs_per_album=5):
    users = session.query(User).all()
    songs = session.query(Song).all()

    for _ in range(album_count):
        album = Album(
            name=fake.sentence(nb_words=3),
            artist=fake.name()
        )
        session.add(album)
        session.commit()

        # Assign random songs to album
        for _ in range(songs_per_album):
            album_song = AlbumSong(album_id=album.id, song_id=random.choice(songs).id)
            session.add(album_song)

    session.commit()
    print(f"✅ Created {album_count} albums and assigned songs.")

# ✅ Create Playlists with Songs
def create_playlists_with_songs(session, playlist_count=10000, songs_per_playlist=5):
    users = session.query(User).all()
    songs = session.query(Song).all()

    for _ in range(playlist_count):
        user = random.choice(users)
        playlist = Playlist(
            name=fake.sentence(nb_words=2),
            user_id=user.id
        )
        session.add(playlist)
        session.commit()

        # Assign random songs to playlist
        for _ in range(songs_per_playlist):
            playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=random.choice(songs).id)
            session.add(playlist_song)

    session.commit()
    print(f"✅ Created {playlist_count} playlists and assigned songs.")

# ✅ Add Songs to Favorites
def add_favorites(session, count=5000):
    users = session.query(User).all()
    songs = session.query(Song).all()

    for _ in range(count):
        user = random.choice(users)
        song = random.choice(songs)
        favorite = Favorite(user_id=user.id, song_id=song.id)
        session.add(favorite)

    session.commit()
    print(f"Added {count} songs to favorites.")

# ✅ Remove Some Albums, Playlists & Songs
def cleanup_data(session, albums_to_remove=500, playlists_to_remove=500):
    albums = session.query(Album).limit(albums_to_remove).all()
    playlists = session.query(Playlist).limit(playlists_to_remove).all()

    for album in albums:
        session.delete(album)

    for playlist in playlists:
        session.delete(playlist)

    session.commit()
    print(f"❌ Removed {albums_to_remove} albums and {playlists_to_remove} playlists.")

# ✅ Run the Script
def run_test_script():
    session = get_session()
    try:
        create_users(session)
        create_songs(session)
        create_albums_with_songs(session)
        create_playlists_with_songs(session)
        add_favorites(session)
        #cleanup_data(session)
        print("🎉 **Database successfully populated with test data!**")
    finally:
        session.close()

if __name__ == "__main__":
    run_test_script()
