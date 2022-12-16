import os

import pytest
from dagster import build_op_context
from dotenv import load_dotenv


@pytest.fixture
def params():
    # env
    load_dotenv(dotenv_path="env")
    updated_at = "2022-12-14"
    op_config = {"updated_at": updated_at}
    context = build_op_context(op_config=op_config)
    context.log.info("Setup pipeline context")

    mysql_db_params = {
        "host": "localhost",
        "port": os.getenv("MYSQL_PORT"),
        "database": os.getenv("MYSQL_DATABASE"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
    }
    psql_db_params = {
        "host": "localhost",
        "port": os.getenv("POSTGRES_PORT"),
        "database": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
    }
    api_params = {
        "username": os.getenv("SPOTIFY_USERNAME"),
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "scope": os.getenv("SPOTIFY_SCOPE"),
    }
    psql_target_db = os.getenv("POSTGRES_DB")
    artists_load_dtypes = {
        "number": "int",
        "artist_popularity": "int",
        "followers": "int",
        "genres": "str",
        "artist_id": "str",
        "name": "str",
        "track_id": "str",
        "track_name_prev": "str",
        "type": "str",
    }
    tracks_load_dtypes = {
        "number0": "int",
        "number": "int",
        "acousticness": "float",
        "album_id": "str",
        "analysis_url": "str",
        "artists_id": "str",
        "country": "str",
        "danceability": "float",
        "disc_number": "int",
        "duration_ms": "int",
        "energy": "float",
        "href": "str",
        "track_id": "str",
        "instrumentalness": "float",
        "track_key": "int",
        "liveness": "float",
        "loudness": "float",
        "mode": "int",
        "name": "str",
        "playlist": "str",
        "popularity": "int",
        "preview_url": "str",
        "speechiness": "float",
        "tempo": "float",
        "time_signature": "int",
        "track_href": "str",
        "track_name_prev": "str",
        "track_number": "int",
        "uri": "str",
        "valence": "float",
        "type": "str",
    }

    return {
        "data_source": "spotify",
        # "domain_name": "marketing",
        "context": context,
        "updated_at": updated_at,
        "mysql_db_params": mysql_db_params,
        "psql_db_params": psql_db_params,
        "api_params": api_params,
        "src_api_params": api_params,
        "src_db_params": mysql_db_params,
        "target_db_params": psql_db_params,
        "target_schema": "spotify",
        "psql_target_db": psql_target_db,
        "s3_bucket": os.getenv("DATALAKE_BUCKET"),
        "artists_load_dtypes": artists_load_dtypes,
        "tracks_load_dtypes": tracks_load_dtypes,
    }
