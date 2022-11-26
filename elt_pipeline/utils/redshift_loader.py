import os
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from utils.data_loader import DataLoader


class RedshiftLoader(DataLoader):

    def get_db_connection(self):
        conn_info = (
                f"postgresql+psycopg2://{self.params['user']}:{self.params['password']}"
                + f"@{self.params['host']}:{self.params['port']}"
                + f"/{self.params['database']}"
        )
        db_conn = create_engine(conn_info)
        return db_conn

    def extract_data(self, sql: str) -> pd.DataFrame:
        pass

    def load_data(self, pd_data: pd.DataFrame, params: dict) -> int:
        src_tbl = f"{params.get('target_schema')}.{params.get('target_tbl')}"
        tmp_tbl = f"{params.get('target_tbl')}_tmp_{datetime.now().strftime('%Y_%m_%d')}"

        # command = f"""
        #         CREATE TEMP TABLE {tmp_tbl} (LIKE {src_tbl});

        #         COPY {tmp_tbl} ("{'","'.join(params.get('ls_columns'))}")
        #         FROM '{params.get("s3_file")}/'
        #         CREDENTIALS 'aws_access_key_id={os.getenv('AWS_ACCESS_KEY_ID')};aws_secret_access_key={os.getenv('AWS_SECRET_ACCESS_KEY')}'
        #         FORMAT AS PARQUET;
        #     """
        command = f"""
                CREATE TEMP TABLE {tmp_tbl} (LIKE {src_tbl});

                COPY {tmp_tbl} ("{'","'.join(params.get('ls_columns'))}")
                FROM '{params.get("s3_file")}'
                CREDENTIALS 'aws_access_key_id={os.getenv('AWS_ACCESS_KEY_ID')};aws_secret_access_key={os.getenv('AWS_SECRET_ACCESS_KEY')}'
                DELIMITER '|' gzip
                DATEFORMAT 'auto'
                REMOVEQUOTES
                IGNOREHEADER 1;        
            """        
        if params.get("primary_keys"):
            conditions = " AND ".join([f""" {src_tbl}."{k}" = {tmp_tbl}."{k}" """ for k in params.get("primary_keys")])
            command += f"""
                BEGIN TRANSACTION;
                DELETE FROM {src_tbl}
                USING {tmp_tbl}
                WHERE {conditions};

                INSERT INTO {src_tbl}
                SELECT * FROM {tmp_tbl};

                END TRANSACTION;    

                DROP TABLE {tmp_tbl};
            """
        else:
            command += f"""
                BEGIN TRANSACTION;
                DELETE FROM {src_tbl};

                INSERT INTO {src_tbl}
                SELECT * FROM {tmp_tbl};

                END TRANSACTION;    

                DROP TABLE {tmp_tbl};
            """

        print(f"SQL: {command}")

        # execute
        db_conn = self.get_db_connection()
        with db_conn.connect() as conn:
            result = conn.execution_options(autocommit=True).execute(command)

        res_code = 1 if result is not None else -1

        return res_code

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
