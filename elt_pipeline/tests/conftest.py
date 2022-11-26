import os

import pytest
from dagster import build_op_context
from dotenv import load_dotenv


@pytest.fixture
def params():
    # env
    load_dotenv(dotenv_path="env.test")
    updated_at = "2018-01-01"
    op_config = {
        "updated_at": updated_at
    }
    context = build_op_context(op_config=op_config)
    context.log.info("Setup pipeline context")

    mysql_db_params = {
        "host": os.getenv("MYSQL_HOST"),
        "port": os.getenv("MYSQL_PORT"),
        "database": os.getenv("MYSQL_DATABASE"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD")
    }
    psql_db_params = {
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
        "database": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD")
    }
    redshift_db_params = {
        "host": os.getenv("DWH_HOST"),
        "port": os.getenv("DWH_PORT"),
        "database": os.getenv("DWH_DB"),
        "user": os.getenv("DWH_USER"),
        "password": os.getenv("DWH_PASSWORD")
    }
    psql_target_db = os.getenv("POSTGRES_DB")
    redshift_target_db = os.getenv("DWH_DB")
    orders_load_dtypes = {
        "order_id": "str",
        "customer_id": "str",
        "order_status": "str",
        "order_purchase_timestamp": "str",
        "order_approved_at": "str",
        "order_delivered_carrier_date": "str",
        "order_delivered_customer_date": "str",
        "order_estimated_delivery_date": "str"
    }

    return {
        "data_source": "ecommerce",
        "domain_name": "marketing",
        "context": context,
        "updated_at": updated_at,
        "mysql_db_params": mysql_db_params,
        "psql_db_params": psql_db_params,
        "redshift_db_params": redshift_db_params,
        "src_db_params": mysql_db_params,
        "target_db_params": psql_db_params,
        "target_schema": "brazillian_ecommerce",
        "psql_target_db": psql_target_db,
        "redshift_target_db": redshift_target_db,
        "s3_bucket": os.getenv("DATALAKE_BUCKET"),
        "orders_load_dtypes": orders_load_dtypes
    }
