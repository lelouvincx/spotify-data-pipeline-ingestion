import pytest
import sys

sys.path.append(
    "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline"
)
from ops.load_data_to_psql import load_data_to_psql


class TestLoadDataToPsql:
    @pytest.fixture
    def psql_params(self, params):
        target_tbl = "spotify_artists"
        upstream = {
            "target_db_params": params.get("psql_db_params"),
            "primary_keys": ["album_id", "artist_id", "track_id"],
            "load_dtypes": params.get("artists_load_dtypes"),
            "ls_columns": [col for col in params.get("artists_load_dtypes")],
            "target_tbl": target_tbl,
            "output_tbl": f"{params.get('target_schema')}.{target_tbl}",
            "s3_file": f"s3://{params.get('s3_bucket')}/bronze/{params.get('data_source')}/{target_tbl}/updated_at={params.get('updated_at')}",
        }
        params.update(upstream)
        return params

    def test_load_data_to_psql(self, psql_params):
        # Upstream
        result = load_data_to_psql(psql_params.get("context"), psql_params)
        assert result == True
        pass
