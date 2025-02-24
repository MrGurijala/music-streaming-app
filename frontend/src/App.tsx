import React, { useState, useEffect } from "react";
import axios from "axios";
import logo from "./logo.svg";
import "./App.css";

interface Song {
  title: string;
  artist: string;
  album: string;
  song_url: string;
}

function App() {
  const [song, setSong] = useState<Song | null>(null);

  useEffect(() => {
    axios
      .get("http://your-api-url/stream/1")
      .then((res) => setSong(res.data))
      .catch((err) => console.error(err));
  }, []);
  return (
    <div className="App">
      {song ? (
        <>
          <h2>
            {song.title} - {song.artist}
          </h2>
          <h4>Album: {song.album}</h4>
          <audio controls>
            <source src={song.song_url} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
