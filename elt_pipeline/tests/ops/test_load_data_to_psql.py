import pytest

from ops.load_data_to_psql import load_data_to_psql


class TestLoadDataToPsql:

    @pytest.fixture
    def psql_params(self, params):
        # upstream
        target_tbl = "olist_orders_dataset"
        upstream = {
            "target_db_params": params.get("psql_db_params"),
            "primary_keys": ["customer_id"],
            "load_dtypes": params.get("orders_load_dtypes"),
            "ls_columns": [col for col in params.get("orders_load_dtypes")],
            "target_tbl": target_tbl,
            "output_tbl": f"{params.get('target_schema')}.{target_tbl}",
            "s3_file": f"s3://{params.get('s3_bucket')}/bronze/{params.get('data_source')}/{params.get('domain_name')}/{target_tbl}/updated_at={params.get('updated_at')}"
        }
        params.update(upstream)
        return params

    def test_load_data_to_psql(self, psql_params):
        # upstream
        result = load_data_to_psql(psql_params.get("context"), psql_params)
        assert result == 1
