from locust import HttpUser, task, between
import random
import string

class MusicStreamUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.username = self._random_username()
        self.password = "test123"
        self.email = f"{self.username}@example.com"
        self.song_id = None
        self.album_id = None
        self.playlist_id = None
        self.user_id = None
        self.token = None
        self.headers = {}
        self._signup_and_login()

    def _random_username(self):
        return "user" + str(random.randint(10000, 99999))

    def _signup_and_login(self):
        signup_resp = self.client.post("/auth/signup", params={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })
        if signup_resp.status_code == 200:
            self.user_id = signup_resp.json().get("user_id")

        login_resp = self.client.post("/auth/login", params={
            "username": self.username,
            "password": self.password
        })
        if login_resp.status_code == 200:
            self.token = login_resp.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(2)
    def view_songs(self):
        resp = self.client.get("/songs", headers=self.headers)
        if resp.status_code == 200 and resp.json():
            self.song_id = resp.json()[0]["id"]

    @task(1)
    def search_songs(self):
        self.client.get("/songs/search", params={"query": "rock"}, headers=self.headers)

    @task(2)
    def stream_song(self):
        if self.song_id:
            self.client.get(f"/songs/{self.song_id}/stream", headers=self.headers)

    @task(1)
    def add_song(self):
        genres = ["classical", "electronic", "pop", "rock"]
        genre = random.choice(genres)
        index = random.randint(1, 100)
        self.client.post("/songs/create", params={
            "title": f"{genre.capitalize()} Song {index}",
            "artist": f"Artist {index}",
            "album": f"{genre.capitalize()} Album {index}",
            "url": f"s3://music-transcoded-bucket/songs/{genre}/{genre}/{index}.mp3"
        }, headers=self.headers)

    @task(1)
    def create_album(self):
        resp = self.client.post("/albums/create", params={
            "name": "Test Album",
            "artist": "Test Artist"
        }, headers=self.headers)
        if resp.status_code == 200:
            self.album_id = resp.json()["album"]["id"]

    @task(1)
    def add_song_to_album(self):
        if self.album_id and self.song_id:
            self.client.post(f"/albums/{self.album_id}/songs", json={"song_id": self.song_id}, headers=self.headers)

    @task(1)
    def remove_song_from_album(self):
        if self.album_id and self.song_id:
            self.client.delete(f"/albums/{self.album_id}/songs/{self.song_id}", headers=self.headers)

    @task(1)
    def delete_album(self):
        if self.album_id:
            self.client.delete(f"/albums/{self.album_id}", headers=self.headers)
            self.album_id = None

    @task(1)
    def create_playlist(self):
        if self.user_id:
            resp = self.client.post("/playlists", json={
                "name": "Locust Playlist",
                "user": {"user_id": self.user_id}
            }, headers=self.headers)
            if resp.status_code == 200:
                self.playlist_id = resp.json()["playlist"]["id"]

    @task(1)
    def add_song_to_playlist(self):
        if self.playlist_id and self.song_id:
            self.client.post(f"/playlists/{self.playlist_id}/songs", json={"song_id": self.song_id}, headers=self.headers)

    @task(1)
    def remove_song_from_playlist(self):
        if self.playlist_id and self.song_id:
            self.client.delete(f"/playlists/{self.playlist_id}/songs/{self.song_id}", headers=self.headers)

    @task(1)
    def delete_playlist(self):
        if self.playlist_id:
            self.client.delete(f"/playlists/{self.playlist_id}", headers=self.headers)
            self.playlist_id = None

    @task(1)
    def add_favorite(self):
        if self.user_id and self.song_id:
            self.client.post(f"/favorites/create/{self.user_id}", json={"song_id": self.song_id}, headers=self.headers)

    @task(1)
    def get_favorites(self):
        if self.user_id:
            self.client.get(f"/favorites/{self.user_id}", headers=self.headers)

    @task(1)
    def remove_favorite(self):
        if self.user_id and self.song_id:
            self.client.delete(f"/favorites/{self.user_id}/{self.song_id}", headers=self.headers)
