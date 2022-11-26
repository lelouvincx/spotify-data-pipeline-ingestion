import pandas as pd

from ops.load_data_to_s3 import load_data_to_s3


class TestLoadDataToS3:

    def test_load_data_to_s3(self, params):
        # upstream
        data_source = params.get('data_source')
        domain_name = params.get('domain_name')
        target_tbl = "olist_orders_dataset"
        pd_data = pd.read_csv("tests/data/olist_orders_dataset.csv", dtype=params.get("orders_load_dtypes"))

        # for psql
        upstream = {
            "load_dtypes": params.get("orders_load_dtypes"),
            "updated_at": params.get("updated_at"),
            "s3_path": f"bronze/{data_source}/{domain_name}/{target_tbl}",
            "data": pd_data
        }
        res = load_data_to_s3(params.get("context"), upstream)
        assert res is not None, "Should be able to load data"