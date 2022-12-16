from dagster import repository

from schedules.schedule_pipeline_ingestion import (
    daily_pipeline_mssql2psql_ingestion,
    daily_pipeline_api2psql_ingestion,
)


@repository
def spotify_data_platform():
    return [daily_pipeline_mssql2psql_ingestion, daily_pipeline_api2psql_ingestion]
