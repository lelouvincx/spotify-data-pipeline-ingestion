import sys

sys.path.append(
    "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline"
)
from ops.extract_data_from_api import extract_data_from_api


class TestExtractDataFromApi:
    def test_extract_data_from_api(self, params):
        result = extract_data_from_api(params.get("context"), params)
        pd_data = result.get("data")
        assert pd_data is not None
        assert (
            pd_data.shape[0] > 0
        ), f"Should have data. Currently returned {pd_data.shape[0]} rows"
