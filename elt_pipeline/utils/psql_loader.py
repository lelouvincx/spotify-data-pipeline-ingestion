import contextlib
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from utils.data_loader import DataLoader


class PsqlLoader(DataLoader):
    @contextlib.contextmanager
    def get_db_connection(self):
        conn_info = (
            f"postgresql+psycopg2://{self.params['user']}:{self.params['password']}"
            + f"@{self.params['host']}:{self.params['port']}"
            + f"/{self.params['database']}"
        )
        print(f"Configs: {conn_info}")
        db_conn = create_engine(conn_info)
        try:
            yield db_conn
        except Exception as e:
            raise e

    def extract_data(self, sql: str) -> pd.DataFrame:
        pd_data = None
        with self.get_db_connection() as db_conn:
            pd_data = pd.read_sql(sql, db_conn)
        return pd_data

    def load_data(self, pd_data: pd.DataFrame, params: dict) -> bool:
        tmp_tbl = (
            f"{params.get('target_tbl')}_tmp_{datetime.now().strftime('%Y_%m_%d')}"
        )
        with self.get_db_connection() as db_conn:
            with db_conn.connect() as cursor:
                # Create temp table
                cursor.execute(
                    f"CREATE TEMP TABLE IF NOT EXISTS {tmp_tbl} (LIKE {params.get('output_tbl')})"
                )

                # Insert new data
                pd_data[params.get("ls_columns")].to_sql(
                    tmp_tbl,
                    db_conn,
                    if_exists="replace",
                    index=False,
                    chunksize=10000,
                    method="multi",
                )

            with db_conn.connect() as cursor:
                # Check if data is inserted
                result = cursor.execute(f"SELECT COUNT(*) FROM {tmp_tbl}")
                for row in result:
                    print(f"Temp table records: {row}")

                    # Upsert data
                    if params.get("primary_keys"):
                        conditions = " AND ".join(
                            [
                                f""" {params.get('output_tbl')}."{k}" = {tmp_tbl}."{k}" """
                                for k in params.get("primary_keys")
                            ]
                        )
                        command = f"""
                            BEGIN TRANSACTION;
                            DELETE FROM {params.get('output_tbl')}
                            USING {tmp_tbl}
                            WHERE {conditions};

                            INSERT INTO {params.get('output_tbl')}
                            SELECT * FROM {tmp_tbl};

                            END TRANSACTION;
                        """
                    else:
                        command = f"""
                            BEGIN TRANSACTION;
                            DELETE FROM {params.get('output_tbl')};

                            INSERT INTO {params.get('output_tbl')}
                            SELECT * FROM {tmp_tbl};

                            END TRANSACTION;
                        """
                    print(f"SQL: {command}")
                    cursor.execute(command)

                    # Drop temp table
                    cursor.execute(f"DROP TABLE IF EXISTS {tmp_tbl}")

        return True

    def get_watermark(self, table_name, watermark: str) -> str:
        sql = f"""
            SELECT MAX({watermark}) AS watermark
            FROM {table_name}
        """
        db_conn = self.get_db_connection()
        pd_data = pd.read_sql(sql, db_conn)
        if len(pd_data) > 0:
            return pd_data.iloc[0]["watermark"]
        return ""
