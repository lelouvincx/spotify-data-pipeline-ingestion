-- Full load reference database
DROP DATABASE IF EXISTS spotify;
CREATE DATABASE spotify;
USE spotify;

-- Albums load
DROP TABLE IF EXISTS spotify.spotify_albums;
CREATE TABLE spotify.spotify_albums (
  number INT,
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
  total_tracks INT,
  track_id VARCHAR(50),
  track_name_prev VARCHAR(50),
  uri VARCHAR(50),
  type VARCHAR(50),
  PRIMARY KEY (album_id)
);

-- Artists load
DROP TABLE IF EXISTS spotify_artists;
CREATE TABLE spotify.spotify_artists (
  number INT,
  artist_popularity INT,
  followers INT,
  genres VARCHAR(128),
  artist_id VARCHAR(50),
  name VARCHAR(50),
  track_id VARCHAR(50),
  track_name_prev VARCHAR(50),
  type VARCHAR(50),
  PRIMARY KEY (artist_id)
);

-- Tracks load
DROP TABLE IF EXISTS spotify.spotify_tracks;
CREATE TABLE spotify.spotify_tracks (
  number0 INT,
  number INT,
  acousticness DOUBLE,
  album_id VARCHAR(50),
  analysis_url VARCHAR(64),
  artists_id VARCHAR(128),
  country CHAR(2),
  danceability DOUBLE,
  disc_number INT,
  duration_ms INT,
  energy DOUBLE,
  href VARCHAR(64),
  track_id VARCHAR(50),
  instrumentalness DOUBLE,
  track_key INT,
  liveness DOUBLE,
  loudness DOUBLE,
  mode INT,
  name VARCHAR(128),
  playlist VARCHAR(50),
  popularity INT,
  preview_url VARCHAR(128),
  speechiness DOUBLE,
  tempo DOUBLE,
  time_signature INT,
  track_href VARCHAR(64),
  track_name_prev VARCHAR(50),
  track_number INT,
  uri VARCHAR(50),
  valence DOUBLE,
  type VARCHAR(50),
  PRIMARY KEY (track_id)
);
