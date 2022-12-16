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


def extract_data_from_mysql(context, run_config):
    updated_at = context.op_config.get("updated_at")
    context.log.info(f"Updated at: {updated_at}")
    if updated_at is None or updated_at == "":
        context.log.info("Nothing to do!")
        return None
    context.log.info(f"Op extracts data from MySQL at {updated_at}")

    # Choose extract strategy (default: full load)
    sql_stm = f"""
        SELECT *
        FROM {run_config.get('src_tbl')}
        WHERE 1=1
    """
    if run_config.get("strategy") == "incremental_by_partition":
        if updated_at != "init_dump":
            sql_stm += f""" AND CAST({run_config.get('partition')} AS DATE) = '{updated_at}' """

    if run_config.get("strategy") == "incremental_by_watermark":
        data_loader = get_data_loader(
            run_config.get("db_provider"), run_config.get("target_db_params")
        )
        watermark = data_loader.get_watermark(
            f"{run_config.get('target_schema')}.{run_config.get('target_tbl')}",
            run_config.get("watermark"),
        )
        watermark = (
            updated_at if watermark is None or watermark > updated_at else watermark
        )
        if updated_at != "init_dump":
            sql_stm += f""" AND {run_config.get('watermark')} >= '{watermark}' """

    context.log.info(f"Extracting with SQL: {sql_stm}")
    db_loader = MysqlLoader(run_config.get("src_db_params"))
    pd_data = db_loader.extract_data(sql_stm)
    context.log.info(f"Data extracted successfully with shape: {pd_data.shape}")

    # Update params
    run_config.update(
        {
            "updated_at": updated_at,
            "data": pd_data,
            "s3_path": f"bronze/{run_config.get('data_source')}/{run_config.get('ls_target').get('target_tbl')}",
            "load_dtypes": run_config.get("load_dtypes"),
        }
    )

    return run_config


def factory_for_extract_data_from_mysql(name, run_config):
    @op(name=name, config_schema={"updated_at": str})
    def _extract_data_from_mysql(context):
        return extract_data_from_mysql(context, run_config)

    return _extract_data_from_mysql
