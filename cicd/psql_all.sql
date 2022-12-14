CREATE SCHEMA IF NOT EXISTS spotify;

DROP TABLE IF EXISTS spotify.spotify_albums CASCADE;
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

DROP TABLE IF EXISTS spotify.spotify_artists CASCADE;
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

DROP TABLE IF EXISTS spotify.spotify_tracks CASCADE;
CREATE TABLE spotify.spotify_tracks (
  number0 INT,
  number INT,
  acousticness DOUBLE PRECISION,
  album_id VARCHAR(50),
  analysis_url VARCHAR(64),
  artists_id VARCHAR(128),
  country CHAR(2),
  danceability DOUBLE PRECISION,
  disc_number INT,
  duration_ms INT,
  energy DOUBLE PRECISION,
  href VARCHAR(64),
  track_id VARCHAR(50),
  instrumentalness DOUBLE PRECISION,
  track_key INT,
  liveness DOUBLE PRECISION,
  loudness DOUBLE PRECISION,
  mode INT,
  name VARCHAR(128),
  playlist VARCHAR(50),
  popularity INT,
  preview_url VARCHAR(128),
  speechiness DOUBLE PRECISION,
  tempo DOUBLE PRECISION,
  time_signature INT,
  track_href VARCHAR(64),
  track_name_prev VARCHAR(50),
  track_number INT,
  uri VARCHAR(50),
  valence DOUBLE PRECISION,
  type VARCHAR(10),
  PRIMARY KEY (track_id)
);

DROP TABLE IF EXISTS spotify.my_tracks CASCADE;
CREATE TABLE spotify.my_tracks (
  album_id VARCHAR(50),
  artists_id VARCHAR(128),
  track_id VARCHAR(50),
  name VARCHAR(128),
  popularity INT,
  type VARCHAR(10),
  duration_ms INT,
  played_at VARCHAR(12),
  danceability DOUBLE PRECISION,
  energy DOUBLE PRECISION,
  track_key INT,
  loudness DOUBLE PRECISION,
  mode INT,
  speechiness DOUBLE PRECISION,
  acousticness DOUBLE PRECISION,
  instrumentalness DOUBLE PRECISION,
  liveness DOUBLE PRECISION,
  valence DOUBLE PRECISION,
  tempo DOUBLE PRECISION,
  PRIMARY KEY (track_id)
);
