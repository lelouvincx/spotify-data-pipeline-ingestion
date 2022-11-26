from utils.mysql_loader import MysqlLoader


class TestMysqlLoader:

    def test_extract_data(self, params):
        sql = "SELECT * FROM olist_orders_dataset LIMIT 10;"
        db_loader = MysqlLoader(params.get("mysql_db_params"))
        pd_data = db_loader.extract_data(sql)
        num_records = pd_data.shape[0]
        assert num_records > 0, f"pd_data should have data, current number of records is {num_records}"
