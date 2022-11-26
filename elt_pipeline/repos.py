from dagster import repository

from schedules.schedule_pipeline_mssql2psql_ingestion import (
    daily_pipeline_mssql2psql_ingestion,
)


@repository
def de_data_platform():
    return [daily_pipeline_mssql2psql_ingestion]
