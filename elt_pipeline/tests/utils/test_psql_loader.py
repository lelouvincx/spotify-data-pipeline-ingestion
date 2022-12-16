import pandas as pd
import sys

sys.path.append(
    "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline"
)
from utils.psql_loader import PsqlLoader


class TestPsqlLoader:
    def test_extract_data(self, params):
        pass

    def test_load_data(self, params):
        target_schema = params.get("target_schema")
        target_tbl = "spotify_artists"

        # Extract data from S3
        upstream = {
            "output_tbl": f"{target_schema}.{target_tbl}",
            "target_tbl": target_tbl,
            "load_dtypes": params.get("spotify_artists"),
            "primary_keys": ["artist_id"],
            "ls_columns": [col for col in params.get("artists_load_dtypes")],
        }
        pd_data = pd.read_csv(
            "elt_pipeline/tests/data/spotify_artists.csv",
            dtype=params.get("artists_load_dtypes"),
        )

        # quick test on 10 records
        pd_data = pd_data.head(10)
        num_records = pd_data.shape[0]
        assert (
            num_records > 0
        ), f"pd_data should have data, current number of records is {num_records}"

        db_loader = PsqlLoader(params.get("psql_db_params"))
        res = db_loader.load_data(pd_data, upstream)
        assert res == True, f"Should be able to load data to PSQL"
