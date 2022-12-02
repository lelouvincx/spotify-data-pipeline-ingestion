ALTER TABLE spotify_albums ADD FOREIGN KEY (artist_id) REFERENCES spotify_artists(artist_id);
ALTER TABLE spotify_albums ADD FOREIGN KEY (track_id) REFERENCES spotify_tracks(track_id);
ALTER TABLE spotify_artists ADD FOREIGN KEY (track_id) REFERENCES spotify_tracks(track_id);
ALTER TABLE spotify_tracks ADD FOREIGN KEY (album_id) REFERENCES spotify_albums(album_id);
