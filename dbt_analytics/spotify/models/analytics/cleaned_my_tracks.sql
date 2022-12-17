{{ config(materialized='table') }}

with my_unique_tracks AS (

  select *
  from spotify.my_tracks
  group by track_unique_id

)

select * from my_unique_tracks
