import pandas as pd
import spotipy
from utils.data_loader import DataLoader
from typing import List
import requests
from os import listdir
import ast


class ApiLoader(DataLoader):
    def get_api_token(self) -> str:
        username = self.params["username"]
        client_id = self.params["client_id"]
        client_secret = self.params["client_secret"]
        redirect_uri = self.params["redirect_uri"]
        scope = self.params["scope"]

        token = spotipy.util.prompt_for_user_token(
            username=username,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
        return token

    def get_streamings(
        self,
        path: str = "/home/lelouvincx/Documents/FundamentalDataEngineering/project/dataset",
    ) -> List[dict]:
        files = [
            "/home/lelouvincx/Documents/FundamentalDataEngineering/project/dataset/" + x
            for x in listdir(path)
            if x.split(".")[0][:-1] == "StreamingHistory"
        ]
        all_streamings = []

        for file in files:
            with open(file, "r", encoding="UTF-8") as f:
                new_streamings = ast.literal_eval(f.read())
                all_streamings += [streaming for streaming in new_streamings]

        return all_streamings

    # Get track's id
    def get_id(self, track_name: str, token: str):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer " + token,
        }
        params = [
            ("q", track_name),
            ("type", "track"),
        ]
        try:
            response = requests.get(
                "https://api.spotify.com/v1/search",
                headers=headers,
                params=params,
                timeout=5,
            )
            json = response.json()
            first_result = json["tracks"]["items"][0]
            track_id = first_result["id"]
            return track_id
        except:
            return None

    def get_features(self, track_id: str, token: str) -> dict:
        sp = spotipy.Spotify(auth=token)
        try:
            features = sp.audio_features([track_id])
            return features[0]
        except:
            return None

    def get_recently(self, number: int, token: str) -> (int, dict):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer " + token,
        }
        params = [
            ("limit", number),
        ]
        try:
            response = requests.get(
                "https://api.spotify.com/v1/me/player/recently-played",
                headers=headers,
                params=params,
                timeout=10,
            )
            return (response.status_code, response.json())
        except:
            return None

    def extract_data(self, token: str) -> pd.DataFrame:
        (code, content) = self.get_recently(50, token)
        my_tracks = {
            "album_id": [],
            "artists_id": [],
            "track_id": [],
            "track_unique_id": [],
            "name": [],
            "popularity": [],
            "type": [],
            "duration_ms": [],
            "played_at": [],
            "danceability": [],
            "energy": [],
            "track_key": [],
            "loudness": [],
            "mode": [],
            "speechiness": [],
            "acousticness": [],
            "instrumentalness": [],
            "liveness": [],
            "valence": [],
            "tempo": [],
        }

        items = content.get("items", [])
        for item in items:
            # Take album_id, artists_id, track_id, name, popularity, type, duration_ms
            played_at = item.get("played_at", [])
            track = item.get("track", [])
            album = track.get("album", [])
            album_id = album.get("id", [])
            artists = track.get("artists", [])
            artists_id = []
            for artist in artists:
                artists_id.append(artist.get("id", []))
            track_id = track.get("id", [])
            name = track.get("name", [])
            popularity = track.get("popularity", [])
            type = track.get("type", [])
            duration_ms = track.get("duration_ms", [])

            # Take features
            features = self.get_features(track_id, token)
            danceability = features.get("danceability", [])
            energy = features.get("energy", [])
            track_key = features.get("key", [])
            loudness = features.get("loudness", [])
            mode = features.get("mode", [])
            speechiness = features.get("speechiness", [])
            acousticness = features.get("acousticness", [])
            instrumentalness = features.get("instrumentalness", [])
            liveness = features.get("liveness", [])
            valence = features.get("valence", [])
            tempo = features.get("tempo", [])

            # Extract row into dict
            my_tracks["album_id"].append(album_id)
            my_tracks["artists_id"].append(artists_id)
            my_tracks["track_id"].append(track_id)
            my_tracks["track_unique_id"].append(track_id + played_at)
            my_tracks["name"].append(name)
            my_tracks["popularity"].append(popularity)
            my_tracks["type"].append(type)
            my_tracks["duration_ms"].append(duration_ms)
            my_tracks["played_at"].append(played_at[:10])
            my_tracks["danceability"].append(danceability)
            my_tracks["energy"].append(energy)
            my_tracks["track_key"].append(track_key)
            my_tracks["loudness"].append(loudness)
            my_tracks["mode"].append(mode)
            my_tracks["speechiness"].append(speechiness)
            my_tracks["acousticness"].append(acousticness)
            my_tracks["instrumentalness"].append(instrumentalness)
            my_tracks["liveness"].append(liveness)
            my_tracks["valence"].append(valence)
            my_tracks["tempo"].append(tempo)

        pd_data = pd.DataFrame(my_tracks)
        return pd_data

    def load_data(self, pd_data: pd.DataFrame, params: dict) -> bool:
        return super().load_data(pd_data, params)

    def get_watermark(self, table_name, watermark: str) -> str:
        return super().get_watermark(table_name, watermark)
