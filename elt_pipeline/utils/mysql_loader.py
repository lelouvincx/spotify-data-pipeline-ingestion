import pandas as pd
from sqlalchemy import create_engine

from utils.data_loader import DataLoader


class MysqlLoader(DataLoader):

    def get_db_connection(self):
        conn_info = (
                f"mysql+pymysql://{self.params['user']}:{self.params['password']}"
                + f"@{self.params['host']}:{self.params['port']}"
                + f"/{self.params['database']}")
        print(f"Configs: {conn_info}")
        db_conn = create_engine(conn_info) 
        return db_conn       

    def extract_data(self, sql: str) -> pd.DataFrame:
        db_conn = self.get_db_connection()
        pd_data = pd.read_sql(sql, db_conn)
        return pd_data

    def load_data(self, pd_data: pd.DataFrame, params: dict) -> int:
        pass

    def get_watermark(self, table_name, watermark: str) -> str:
        pass
