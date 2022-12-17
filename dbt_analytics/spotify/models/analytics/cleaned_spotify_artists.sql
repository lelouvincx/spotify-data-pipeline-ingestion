{{ config(materialized='table') }}

with unique_artists AS (

  select artist_popularity, followers, genres, artist_id, name, track_id
  from spotify.spotify_artists
  group by artist_id

)

select * from unique_artists
