import json
import os
from datetime import datetime

from dagster import op, job, daily_partitioned_config

from ops.extract_data_from_mysql import factory_for_extract_data_from_mysql
from ops.load_data_to_psql import factory_for_load_data_to_psql
from ops.load_data_to_redshift import factory_for_load_data_to_redshift
from ops.load_data_to_s3 import factory_for_load_data_to_s3


@op
def validating_mssql2psql_ingestion(context, statuses):
    context.log.info(f"Done. {statuses}")
    if len([-1 for s in statuses if s is not None and "-1" in str(s)]) > 0:
        raise Exception("Sorry, no numbers below zero")


@daily_partitioned_config(start_date=datetime(2022, 10, 1), timezone="Asia/Ho_Chi_Minh")
def get_partitioned_config(start: datetime, _end: datetime):
    # read metadata
    with open("pipelines/metadata/mssql2psql_ingestion.json", "r") as f0:
        metadata = json.load(f0)

    start = start.strftime("%Y-%m-%d")
    partitions_map = {}
    for table, run_config in metadata:
        partitions_map[f"extract_mysql_{table}"] = {"config": {"created_at": start}}

    run_config = {
        "ops": partitions_map
    }
    return run_config


@job(config=get_partitioned_config)
def job_mssql2psql_ingestion():
    # read metadata
    with open("pipelines/metadata/mssql2psql_ingestion.json", "r") as f0:
        metadata = json.load(f0)

    op_outputs = []
    for table, run_config in metadata:
        # source
        run_config["data_source"] = "ecommerce"
        run_config["domain_name"] = "marketing"
        run_config["src_db_params"] = {
            "host": os.getenv("MYSQL_HOST"),
            "port": os.getenv("MYSQL_PORT"),
            "database": os.getenv("MYSQL_DATABASE"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD")
        }
        extract_data = factory_for_extract_data_from_mysql(f"extract_mysql_{table}", run_config)
        load_to_s3 = factory_for_load_data_to_s3(f"load_mysql_{table}_to_s3")
        landing_step = load_to_s3(extract_data())

        for target_run_config in run_config.get("ls_target"):
            # target
            db_provider = target_run_config.get("db_provider")
            if target_run_config.get("db_provider") == "psql":
                run_config["target_db"] = os.getenv("POSTGRES_DB")
                run_config["target_db_params"] = {
                    "host": os.getenv("POSTGRES_HOST"),
                    "port": os.getenv("POSTGRES_PORT"),
                    "database": os.getenv("POSTGRES_DB"),
                    "user": os.getenv("POSTGRES_USER"),
                    "password": os.getenv("POSTGRES_PASSWORD")
                }
                load_to_target = factory_for_load_data_to_psql(f"load_s3_{table}_to_{db_provider}")
            elif target_run_config.get("db_provider") == "redshift":
                run_config["target_db"] = os.getenv("DWH_DB")
                run_config["target_db_params"] = {
                    "host": os.getenv("DWH_HOST"),
                    "port": os.getenv("DWH_PORT"),
                    "database": os.getenv("DWH_DB"),
                    "user": os.getenv("DWH_USER"),
                    "password": os.getenv("DWH_PASSWORD")
                }
                load_to_target = factory_for_load_data_to_redshift(f"load_s3_{table}_to_{db_provider}")
            else:
                raise ValueError("db_provider should be 'psql' or 'redshift' for getting params!")

            # update target config
            run_config.update(target_run_config)
            run_config["output_tbl"] = f"{run_config.get('target_schema')}.{run_config.get('target_tbl')}"

            # load schema
            with open(f"pipelines/schema/{run_config.get('schema')}.json", "r") as f0:
                schema = json.load(f0)
                run_config["primary_keys"] = schema.get("primary_keys")
                run_config["load_dtypes"] = schema.get("load_dtypes")
                run_config["ls_columns"] = [col for col in run_config.get("load_dtypes")]

            # DAGs ops
            staging_step = load_to_target(landing_step)
            op_outputs.append(staging_step)

    validating_mssql2psql_ingestion(op_outputs)
