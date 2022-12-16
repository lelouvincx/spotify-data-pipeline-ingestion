-- Full load reference database
DROP DATABASE IF EXISTS spotify;
CREATE DATABASE spotify;
USE spotify;

-- Albums load
DROP TABLE IF EXISTS spotify.spotify_albums;
CREATE TABLE spotify.spotify_albums (
  number INT4,
  album_type VARCHAR(50),
  artist_id VARCHAR(50),
  available_markets VARCHAR(512),
  external_urls VARCHAR(128),
  href VARCHAR(64),
  album_id VARCHAR(50),
  images VARCHAR(512),
  name VARCHAR(128),
  release_date VARCHAR(50),
  release_date_precision VARCHAR(50),
  total_tracks INT4,
  track_id VARCHAR(50),
  track_name_prev VARCHAR(50),
  uri VARCHAR(50),
  type VARCHAR(50),
  PRIMARY KEY (album_id)
);

DROP TABLE IF EXISTS spotify_artists;
CREATE TABLE spotify.spotify_artists (
  number INT4,
  artist_popularity INT4,
  followers INT4,
  genres VARCHAR(128),
  artist_id VARCHAR(50),
  name VARCHAR(50),
  track_id VARCHAR(50),
  track_name_prev VARCHAR(50),
  type VARCHAR(50),
  PRIMARY KEY (artist_id)
);

DROP TABLE IF EXISTS spotify.spotify_tracks;
CREATE TABLE spotify.spotify_tracks (
  number0 INT4,
  number INT4,
  acousticness DOUBLE,
  album_id VARCHAR(50),
  analysis_url VARCHAR(64),
  artists_id VARCHAR(128),
  country CHAR(2),
  danceability DOUBLE,
  disc_number INT4,
  duration_ms INT4,
  energy DOUBLE,
  href VARCHAR(64),
  track_id VARCHAR(50),
  instrumentalness DOUBLE,
  track_key INT4,
  liveness DOUBLE,
  loudness DOUBLE,
  mode INT4,
  name VARCHAR(128),
  playlist VARCHAR(50),
  popularity INT4,
  preview_url VARCHAR(128),
  speechiness DOUBLE,
  tempo DOUBLE,
  time_signature INT4,
  track_href VARCHAR(64),
  track_name_prev VARCHAR(50),
  track_number INT4,
  uri VARCHAR(50),
  valence DOUBLE,
  type VARCHAR(50),
  PRIMARY KEY (track_id)
);
