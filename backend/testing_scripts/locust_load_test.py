from locust import HttpUser, task, between
import random

class MusicStreamUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        user_id = random.randint(10000, 99999)
        username = f"user{user_id}"
        password = "test123"
        email = f"{username}@example.com"

        # Sign up the user
        signup_response = self.client.post("/auth/signup", params={
            "username": username,
            "email": email,
            "password": password
        })

        if signup_response.status_code == 200:
            try:
                self.user_id = signup_response.json().get("user_id")
            except Exception:
                self.user_id = None
        else:
            self.user_id = None

        self.username = username
        self.password = password

        # Login and get token
        login_response = self.client.post("/auth/login", params={
            "username": username,
            "password": password
        })

        if login_response.status_code == 200:
            try:
                self.token = login_response.json().get("access_token")
                self.headers = {"Authorization": f"Bearer {self.token}"}
            except Exception:
                self.token = None
                self.headers = {}
        else:
            self.token = None
            self.headers = {}

    @task
    def get_songs(self):
        self.client.get("/songs")

    @task
    def get_song(self):
        self.client.get("/songs/1")

    @task
    def search_songs(self):
        self.client.get("/songs/search?query=love")

    @task
    def stream_song(self):
        self.client.get("/songs/1/stream")

    @task
    def create_album(self):
        self.client.post("/albums/create", params={
            "name": "My Album",
            "artist": "Some Artist"
        })

    @task
    def get_albums(self):
        self.client.get("/albums")

    @task
    def get_album_details(self):
        self.client.get("/albums/1")

    @task
    def add_song_to_album(self):
        self.client.post("/albums/1/songs", json={"song_id": 1})

    @task
    def remove_song_from_album(self):
        self.client.delete("/albums/1/songs/1")

    @task
    def delete_album(self):
        self.client.delete("/albums/1")

    @task
    def create_playlist(self):
        if self.user_id:
            self.client.post("/playlists", json={
                "name": "Locust Playlist",
                "user": {"user_id": self.user_id}
            }, headers=self.headers)

    @task
    def get_user_playlists(self):
        if self.user_id:
            self.client.get(f"/playlists/user/{self.user_id}", headers=self.headers)

    @task
    def add_song_to_playlist(self):
        self.client.post("/playlists/1/songs", json={"song_id": 1}, headers=self.headers)

    @task
    def remove_song_from_playlist(self):
        self.client.delete("/playlists/1/songs/1", headers=self.headers)

    @task
    def delete_playlist(self):
        self.client.delete("/playlists/1", headers=self.headers)

    @task
    def add_favorite(self):
        if self.user_id:
            self.client.post(f"/favorites/create/{self.user_id}", json={"song_id": 1}, headers=self.headers)

    @task
    def get_favorites(self):
        if self.user_id:
            self.client.get(f"/favorites/{self.user_id}", headers=self.headers)

    @task
    def remove_favorite(self):
        if self.user_id:
            self.client.delete(f"/favorites/{self.user_id}/1", headers=self.headers)
