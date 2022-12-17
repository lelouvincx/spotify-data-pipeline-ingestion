import json
import os
from datetime import datetime
from dagster import op, job, daily_partitioned_config

from ops.extract_data_from_mysql import factory_for_extract_data_from_mysql
from ops.load_data_to_psql import factory_for_load_data_to_psql
from ops.load_data_to_s3 import factory_for_load_data_to_s3
from ops.trigger_dbt_spotify import trigger_dbt_spotify


@op
def validate_mssql2psql_ingestion(context, statuses):
    context.log.info(f"Done. {statuses}")
    if len([-1 for s in statuses if s is not None and "-1" in str(s)]) > 0:
        raise Exception("Sorry, no numbers below zero.")
    return True


@daily_partitioned_config(
    start_date=datetime(2022, 12, 11), timezone="Asia/Ho_Chi_Minh"
)
def get_partitioned_config(start: datetime, _end: datetime):
    # Read metadata
    with open("pipelines/metadata/mssql2psql_ingestion.json") as f:
        metadata = json.load(f)

    partition_map = {}
    for table, run_config in metadata:
        partition_map[f"extract_api_{table}"] = {
            "config": {
                "updated_at": start.strftime("%Y-%m-%d"),
            }
        }

    run_config = {"ops": partition_map}
    return run_config


@job(config=get_partitioned_config)
def job_mssql2psql_ingestion():
    # Read metadata
    with open("pipelines/metadata/mssql2psql_ingestion.json", "r") as f:
        metadata = json.load(f)

    op_outputs = []
    for table, run_config in metadata:
        # Source
        run_config["data_source"] = "spotify"
        # run_config['domain_name'] =
        run_config["src_db_params"] = {
            "host": os.getenv("MYSQL_HOST"),
            "port": os.getenv("MYSQL_PORT"),
            "database": os.getenv("MYSQL_DATABASE"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
        }
        extract_data = factory_for_extract_data_from_mysql(
            f"extract_mysql_{table}", run_config
        )  # Return new run_config
        load_to_s3 = factory_for_load_data_to_s3(f"load_mysql_{table}_to_s3")
        landing_step = load_to_s3(extract_data())  # Return upstream

        # TODO: load to psql
        # for target_run_config in run_config.get("ls_target"):
        # with run_config.get("ls_target") as target_run_config:
        target_run_config = run_config.get("ls_target")
        # WARN: Change target_run_config here
        # Target
        db_provider = target_run_config.get("db_provider")
        if db_provider == "psql":
            run_config["target_db"] = os.getenv("POSTGRES_DB")
            run_config["target_db_params"] = {
                "host": os.getenv("POSTGRES_HOST"),
                "port": os.getenv("POSTGRES_PORT"),
                "database": os.getenv("POSTGRES_DB"),
                "user": os.getenv("POSTGRES_USER"),
                "password": os.getenv("POSTGRES_PASSWORD"),
            }
            load_to_target = factory_for_load_data_to_psql(
                f"load_s3_{table}_to_{db_provider}"
            )
        else:
            raise ValueError(
                f"db_provider should be 'psql' for getting environment params! Current is {db_provider}"
            )

        # Update target config
        run_config.update(target_run_config)
        # run_config[
        #     "output_tbl"
        # ] = f"{run_config.get('target_schema')}.{run_config.get('target_tbl')}"
        run_config["output_tbl"] = '"{}"."{}"'.format(
            run_config.get("target_schema"), run_config.get("target_tbl")
        )

        # Load schema
        with open(f"pipelines/schema/{run_config.get('schema')}.json", "r") as f:
            schema = json.load(f)
            run_config["primary_keys"] = schema.get("primary_keys")
            run_config["load_dtypes"] = schema.get("load_dtypes")
            run_config["ls_columns"] = [col for col in run_config.get("load_dtypes")]

        # DAGs ops
        staging_step = load_to_target(landing_step)
        op_outputs.append(staging_step)

    validated = validate_mssql2psql_ingestion(op_outputs)
    trigger_dbt_spotify(validated)
