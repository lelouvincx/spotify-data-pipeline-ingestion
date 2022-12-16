import pandas as pd
import sys

sys.path.append(
    "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline"
)
from ops.load_data_to_s3 import load_data_to_s3


class TestLoadDataToS3:
    def test_load_data_to_s3(self, params):
        # Upstream
        data_source = params.get("data_source")
        # domain_name = params.get("domain_name")
        target_tbl = "spotify_tracks"
        pd_data = pd.read_csv(
            "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline/tests/data/spotify_tracks.csv",
            dtype=params.get("tracks_load_dtypes"),
        )

        # For psql
        upstream = {
            "load_dtypes": params.get("tracks_load_dtypes"),
            "updated_at": params.get("updated_at"),
            "s3_path": f"bronze/{data_source}/{target_tbl}",
            "data": pd_data,
        }
        res = load_data_to_s3(params.get("context"), upstream)
        assert res is not None, "Should be able to load data"
