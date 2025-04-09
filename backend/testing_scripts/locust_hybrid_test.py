
from locust import HttpUser, task, between, events
import random
import string
import requests
import time

AUTH_API = "https://q17ncm6dm3.execute-api.eu-west-2.amazonaws.com/Prod/auth"
SONGS_API = "https://97f405euii.execute-api.eu-west-2.amazonaws.com/Prod/songs"

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
        self._signup_and_login()

    def _random_username(self):
        return "user" + str(random.randint(10000, 99999))

    def _signup_and_login(self):
        # Signup
        signup_url = f"{AUTH_API}/signup"
        start_time = time.time()
        try:
            resp = requests.post(signup_url, params={
                "username": self.username,
                "email": self.email,
                "password": self.password
            })
            if resp.status_code == 200:
                self.user_id = resp.json().get("user_id")
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type="POST", name="/auth/signup", response_time=total_time, response_length=0, exception=None if resp.ok else Exception("Signup failed"))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type="POST", name="/auth/signup", response_time=total_time, response_length=0, exception=e)

        # Login
        login_url = f"{AUTH_API}/login"
        start_time = time.time()
        try:
            resp = requests.post(login_url, params={
                "username": self.username,
                "password": self.password
            })
            if resp.status_code == 200:
                self.token = resp.json().get("access_token")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            else:
                self.token = None
                self.headers = {}
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type="POST", name="/auth/login", response_time=total_time, response_length=0, exception=None if resp.ok else Exception("Login failed"))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type="POST", name="/auth/login", response_time=total_time, response_length=0, exception=e)

    @task(2)
    def view_songs(self):
        url = f"{SONGS_API}/"
        start_time = time.time()
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200 and resp.json():
                self.song_id = resp.json()[0]["id"]
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type="GET", name="/songs", response_time=total_time, response_length=0, exception=None if resp.ok else Exception("View songs failed"))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(request_type="GET", name="/songs", response_time=total_time, response_length=0, exception=e)

    @task(1)
    def search_songs(self):
        url = f"{SONGS_API}/search"
        requests.get(url, params={"query": "rock"}, headers=self.headers)

    @task(2)
    def stream_song(self):
        if self.song_id:
            url = f"{SONGS_API}/{self.song_id}/stream"
            requests.get(url, headers=self.headers)

    @task(1)
    def add_song(self):
        genres = ["classical", "electronic", "pop", "rock"]
        genre = random.choice(genres)
        index = random.randint(1, 100)
        url = f"{SONGS_API}/create"
        requests.post(url, params={
            "title": f"{genre.capitalize()} Song {index}",
            "artist": f"Artist {index}",
            "album": f"{genre.capitalize()} Album {index}",
            "url": f"s3://music-transcoded-bucket/songs/{genre}/{genre}/{index}.mp3"
        }, headers=self.headers)

    # The rest use the ALB host from --host
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
    def create_playlist(self):
        if self.user_id:
            resp = self.client.post("/playlists/create", json={
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
    def add_favorite(self):
        if self.user_id and self.song_id:
            self.client.post(f"/favorites/create/{self.user_id}", json={"song_id": self.song_id}, headers=self.headers)

    @task(1)
    def get_favorites(self):
        if self.user_id:
            self.client.get(f"/favorites/{self.user_id}", headers=self.headers)