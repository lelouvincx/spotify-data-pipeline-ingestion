import os
import pyarrow as pa
import pyarrow.parquet as pq
from dagster import op
import numpy as np


def load_data_to_s3(context, upstream):
    if upstream is None:
        return None

    updated_at = upstream.get("updated_at")
    s3_bucket = os.getenv("DATALAKE_BUCKET")
    if type(updated_at) == list:
        updated_at = max(updated_at)
    s3_file = f"s3://{s3_bucket}/{upstream.get('s3_path')}/updated_at={updated_at}"
    context.log.info(f"Loading data to S3: {s3_file}")

    # Load data to S3
    pd_data = upstream.get("data")

    # Preprocess data
    load_dtypes = upstream.get("load_dtypes")
    try:
        for col, data_type in load_dtypes.items():
            if data_type == "str":
                pd_data[col] = pd_data[col].fillna("")
                pd_data[col] = pd_data[col].astype(str)
                pd_data[col] = pd_data[col].str.strip()
                pd_data[col] = pd_data[col].str.rstrip()
                pd_data[col] = pd_data[col].str.replace("'", "")
                pd_data[col] = pd_data[col].str.replace('"', "")
                pd_data[col] = pd_data[col].str.replace(r"\n", "", regex=True)
            elif data_type == "int":
                cur_bit = np.log2(pd_data[col].max())
                if cur_bit > 32:
                    pd_data[col] = pd_data[col].astype({col: "int64"})
                elif cur_bit > 16:
                    pd_data[col] = pd_data[col].astype({col: "int32"})
                elif cur_bit > 8:
                    pd_data[col] = pd_data[col].astype({col: "int16"})
                else:
                    pd_data[col] = pd_data[col].astype({col: "int8"})
            elif data_type == "float":
                pd_data[col] = pd_data[col].astype({col: "float32"})
        context.log.info(f"Data preprocessed successfully")
    except Exception as e:
        context.log.info(f"Exception: {e}")

    # Write parquet object to S3
    pa_data = pa.Table.from_pandas(df=pd_data, preserve_index=False)
    pq.write_table(pa_data, s3_file)
    context.log.info("Data loaded successfully to S3")

    # Update stream
    upstream.update({"s3_bucket": s3_bucket, "s3_file": s3_file})

    return upstream


def factory_for_load_data_to_s3(name):
    @op(name=name)
    def _load_data_to_s3(context, upstream):
        return load_data_to_s3(context, upstream)

    return _load_data_to_s3
