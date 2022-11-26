import pandas as pd

from utils.psql_loader import PsqlLoader


class TestPsqlLoader:

    def test_extract_data(self, params):
        sql = "SELECT * FROM brazillian_ecommerce.olist_orders_dataset LIMIT 10"
        db_loader = PsqlLoader(params.get("psql_db_params"))
        pd_data = db_loader.extract_data(sql)
        num_records = pd_data.shape[0]
        assert num_records > 0, f"pd_data should have data, current number of records is {num_records}"

    def test_load_data(self, params):
        target_schema = params.get("target_schema")
        target_tbl = "olist_orders_dataset"

        # extract data from S3
        upstream = {
            "output_tbl": f"{target_schema}.{target_tbl}",
            "target_tbl": target_tbl,
            "load_dtypes": params.get("orders_load_dtypes"),
            "primary_keys": ["order_id"],
            "ls_columns": [col for col in params.get("orders_load_dtypes")]
        }
        pd_data = pd.read_csv("tests/data/olist_orders_dataset.csv", dtype=params.get("orders_load_dtypes"))

        # quick test on 10 records
        pd_data = pd_data.head(10)
        num_records = pd_data.shape[0]
        assert num_records > 0, f"pd_data should have data, current number of records is {num_records}"

        db_loader = PsqlLoader(params.get("psql_db_params"))
        res = db_loader.load_data(pd_data, upstream)
        assert res == 1, f"Should be able to load data to PSQL"
