import pytest

from ops.load_data_to_redshift import load_data_to_redshift


class TestLoadDataToRedshift:

    @pytest.fixture
    def redshift_params(self, params):
        # upstream
        target_tbl = "olist_orders_dataset"
        upstream = {
            "target_db_params": params.get("redshift_db_params"),
            "target_schema": params.get('target_schema'),
            "primary_keys": ["order_id"],
            "load_dtypes": params.get("orders_load_dtypes"),
            "ls_columns": [col for col in params.get("orders_load_dtypes")],
            "target_tbl": target_tbl,
            "s3_file": f"s3://{params.get('s3_bucket')}/bronze/{params.get('data_source')}/{params.get('domain_name')}/{target_tbl}/updated_at={params.get('updated_at')}"
        }
        params.update(upstream)
        return params

    def test_load_data_to_redshift(self, redshift_params):
        # upstream
        result = load_data_to_redshift(redshift_params.get("context"), redshift_params)
        assert result == 1
