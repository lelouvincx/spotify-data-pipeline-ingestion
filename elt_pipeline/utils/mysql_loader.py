import pandas as pd
from sqlalchemy import create_engine
import contextlib
from utils.data_loader import DataLoader


class MysqlLoader(DataLoader):
    @contextlib.contextmanager
    def get_db_connection(self):
        conn_info = (
            f"mysql+pymysql://{self.params['user']}:{self.params['password']}"
            + f"@{self.params['host']}:{self.params['port']}"
            + f"/{self.params['database']}"
        )
        print(f"Configs: {conn_info}")
        db_conn = create_engine(conn_info).connect()
        try:
            yield db_conn
        except Exception:
            raise
        finally:
            db_conn.close()

    def extract_data(self, sql: str) -> pd.DataFrame:
        pd_data = None
        with self.get_db_connection() as db_conn:
            pd_data = pd.read_sql(sql, db_conn)
        return pd_data

    def load_data(self, pd_data: pd.DataFrame, params: dict) -> bool:
        return super().load_data(pd_data, params)

    def get_watermark(self, table_name, watermark: str) -> str:
        return super().get_watermark(table_name, watermark)
