import sys
from utils.api_loader import ApiLoader

sys.path.append(
    "/home/lelouvincx/Documents/FundamentalDataEngineering/project/elt_pipeline"
)


class TestApiLoader:
    def test_get_api_token(self, params):
        api_loader = ApiLoader(params.get("api_params"))
        token = api_loader.get_api_token()
        assert token is not None, f"Must return token. Current token is {token}"

    # NOTE: Not need right now
    # def test_get_streamings(self, params):
    #     api_loader = ApiLoader(params.get("api_params"))
    #     streamings = api_loader.get_streamings()
    #     assert (
    #         len(streamings) > 0
    #     ), f"Must return history streamings. Currently return {len(streamings)} streamings"

    def test_get_id(self, params):
        api_loader = ApiLoader(params.get("api_params"))
        token = api_loader.get_api_token()
        track_name = "Perfect"
        track_id = api_loader.get_id(track_name, token)
        assert (
            track_id is not None
        ), f"Must return track's id. Current track's id is {track_id}"

    def test_get_features(self, params):
        api_loader = ApiLoader(params.get("api_params"))
        token = api_loader.get_api_token()
        track_id = "0tgVpDi06FyKpA1z0VMD4v"
        track_features = api_loader.get_features(track_id, token)
        assert (
            track_features is not None
        ), f"Must return track' features. Current track' features are {track_features}"

    def test_get_recently(self, params):
        api_loader = ApiLoader(params.get("api_params"))
        token = api_loader.get_api_token()
        (code, content) = api_loader.get_recently(1, token)
        assert code == 200, f"Request has not succeeded. Current status code is {code}"

    def test_extract_data(self, params):
        api_loader = ApiLoader(params.get("api_params"))
        token = api_loader.get_api_token()
        pd_data = api_loader.extract_data(token)
        rows = pd_data.shape[0]
        assert rows > 0, f"Must return extracted data, currently return {rows} rows"
