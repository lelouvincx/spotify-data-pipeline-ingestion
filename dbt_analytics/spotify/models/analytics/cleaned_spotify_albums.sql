{{ config(materialized='table') }}

with unique_albums AS (

  select album_id, artist_id, album_type, name, release_date, release_date_precision, total_tracks, track_id
  from spotify.spotify_albums
  group by album_id

)

select * from unique_albums
