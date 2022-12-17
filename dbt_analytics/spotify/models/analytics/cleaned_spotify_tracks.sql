{{ config(materialized='table') }}

with unique_tracks AS (

  select acousticness, album_id, artists_id, country, danceability, duration_ms, energy, track_id, instrumentalness, track_key, liveness, loudness, mode, name, popularity, speechiness, tempo, valence
  from spotify.spotify_tracks
  group by track_id

)

select * from unique_tracks
