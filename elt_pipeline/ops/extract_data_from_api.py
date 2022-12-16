from dagster import op

from utils.api_loader import ApiLoader
from utils.mysql_loader import MysqlLoader
from utils.psql_loader import PsqlLoader


# Factory method
def get_data_loader(data_loader: str, params: dict):
    if data_loader == "mysql":
        return MysqlLoader(params)
    elif data_loader == "api":
        return ApiLoader(params)
    elif data_loader == "psql":
        return PsqlLoader(params)
    else:
        raise ValueError(data_loader)


def extract_data_from_api(context, run_config):
    updated_at = context.op_config.get("updated_at")
    context.log.info(f"Updated at: {updated_at}")
    if updated_at is None or updated_at == "":
        context.log.info("Nothing to do!")
        return None
    context.log.info(f"Op extracts data from API at {updated_at}")

    # Extract strategy (only support incremental_by_partition)
    context.log.info(f"Extracting on date: {updated_at}")
    api_loader = ApiLoader(run_config.get("src_api_params"))
    token = api_loader.get_api_token()
    pd_data = api_loader.extract_data(token)
    index_played_at = pd_data[pd_data["played_at"] != updated_at].index  # Drop data
    pd_data.drop(index_played_at, inplace=True)
    context.log.info(
        f"Data loaded and filtered successfully with shape: {pd_data.shape}"
    )

    run_config.update(
        {
            "updated_at": updated_at,
            "data": pd_data,
            "s3_path": f"bronze/{run_config.get('data_source')}/{run_config.get('ls_target').get('target_tbl')}",
            "load_dtypes": run_config.get("load_dtypes"),
        }
    )

    return run_config


def factory_for_extract_data_from_api(name, run_config):
    @op(name=name, config_schema={"updated_at": str})
    def _extract_data_from_api(context):
        return extract_data_from_api(context, run_config)

    return _extract_data_from_api
