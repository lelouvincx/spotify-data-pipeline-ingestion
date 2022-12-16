import sys

sys.path.append(
    "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline"
)
from ops.extract_data_from_mysql import extract_data_from_mysql


class TestExtractDataFromMysql:
    def test_extract_data_from_mysql(self, params):
        run_config = {
            "src_tbl": "spotify_artists",
            "target_tbl": "spotify_artists",
            "strategy": "full_load",
            "target_db": params.get("psql_target_db"),
        }
        params.update(run_config)

        res = extract_data_from_mysql(params.get("context"), params)
        pd_data = res.get("data")
        assert pd_data is not None, "Should be able to get data"
        assert (
            pd_data.shape[0] > 0
        ), f"Should have data. Currently returned {pd_data.shape[0]} rows"
