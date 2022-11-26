import os

from dagster import op


def load_data_to_s3(context, upstream):
    if upstream is None:
        return None

    updated_at = upstream.get("updated_at")
    s3_bucket = os.getenv("DATALAKE_BUCKET")
    if type(updated_at) == list:
        updated_at = max(updated_at)
    s3_file = f"s3://{s3_bucket}/{upstream.get('s3_path')}/updated_at={updated_at}"
    context.log.info(f"Load data to S3: {s3_file}")

    # Load data to S3
    pd_data = upstream.get("data")

    # preprocess data
    load_dtypes = upstream.get('load_dtypes')
    for col, data_type in load_dtypes.items():
        if data_type == "str":
            pd_data[col] = pd_data[col].fillna("")
            pd_data[col] = pd_data[col].astype(str)
            pd_data[col] = pd_data[col].str.strip()
            pd_data[col] = pd_data[col].str.rstrip()
            pd_data[col] = pd_data[col].str.replace("'", "")
            pd_data[col] = pd_data[col].str.replace('"', "")
            pd_data[col] = pd_data[col].str.replace('|', "")
            pd_data[col] = pd_data[col].str.replace('\\', "")
            # remove new line character
            pd_data[col] = pd_data[col].str.replace(r'\n', '', regex=True)

    # pd_data.to_parquet(s3_file)
    pd_data.to_csv(s3_file, sep="|", index=False, compression="gzip")

    # update params
    upstream.update({
        "s3_bucket": s3_bucket,
        "s3_file": s3_file
    })

    return upstream


def factory_for_load_data_to_s3(name):
    @op(name=name)
    def _load_data_to_s3(context, upstream):
        return load_data_to_s3(context, upstream)

    return _load_data_to_s3
