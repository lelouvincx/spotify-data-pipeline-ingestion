import pandas as pd
from dagster import op

from utils.psql_loader import PsqlLoader


def load_data_to_psql(context, upstream):
    if upstream is None:
        return None

    # Load data to target
    context.log.info("Loading data to postgreSQL")
    context.log.info(f"Extracting data from {upstream.get('s3_file')}")
    pd_stag = pd.read_parquet(upstream.get("s3_file"))
    context.log.info(f"Extracted data shape: {pd_stag.shape}")

    if len(pd_stag) == 0:
        context.log.info("No data to upload!")
        return "No data to upload!"

    # Execute
    db_loader = PsqlLoader(upstream.get("target_db_params"))
    result = db_loader.load_data(pd_stag, upstream)
    context.log.info(f"Batch inserted status: {result}")
    return result


def factory_for_load_data_to_psql(name):
    @op(name=name)
    def _load_data_to_psql(context, upstream):
        return load_data_to_psql(context, upstream)

    return _load_data_to_psql
