import os

from ops.extract_data_from_mysql import extract_data_from_mysql


class TestExtractDataFromMysql:

    def test_extract_data_from_mysql_incremental(self, params):
        run_config = {
            "src_tbl": "olist_orders_dataset",
            "target_tbl": "olist_orders_dataset",
            "strategy": "incremental_by_partition",
            "partition": "order_purchase_timestamp",
            "target_db": params.get("psql_target_db")
        }
        params.update(run_config)

        res = extract_data_from_mysql(params.get("context"), params)
        pd_data = res.get("data")
        assert pd_data is not None, "Should be able to get data"
        assert pd_data.shape[0] > 0, "Should have data"

    def test_extract_data_from_mysql_full_load(self, params):
        run_config = {
            "src_tbl": "product_category_name_translation",
            "target_tbl": "product_category_name_translation",
            "strategy": "full_load",
            "target_db": params.get("psql_target_db")
        }
        params.update(run_config)

        res = extract_data_from_mysql(params.get("context"), params)
        pd_data = res.get("data")
        assert pd_data is not None, "Should be able to get data"
        assert pd_data.shape[0] > 0, "Should have data"

    def test_extract_data_from_mysql_watermark(self, params):
        run_config = {
            "src_tbl": "olist_orders_dataset",
            "target_tbl": "olist_orders_dataset",
            "strategy": "incremental_by_watermark",
            "watermark": "order_delivered_customer_date",
            "db_provider": "psql",
            "target_db": params.get("psql_target_db")
        }
        params.update(run_config)

        res = extract_data_from_mysql(params.get("context"), params)
        pd_data = res.get("data")
        assert pd_data is not None, "Should be able to get data"
        assert pd_data.shape[0] > 0, "Should have data"
