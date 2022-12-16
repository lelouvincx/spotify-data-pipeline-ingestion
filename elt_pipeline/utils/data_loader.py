import pandas as pd


class DataLoader:
    def __init__(self, params):
        self.params = params

    def get_api_token(self) -> str:
        pass

    def get_db_connection(self):
        pass

    def extract_data(self, sql: str) -> pd.DataFrame:
        pass

    def load_data(self, pd_data: pd.DataFrame, params: dict) -> bool:
        pass

    def get_watermark(self, table_name, watermark: str) -> str:
        pass
