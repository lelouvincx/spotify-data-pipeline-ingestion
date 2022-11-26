from dagster import build_schedule_from_partitioned_job

# daily schedule
from pipelines.pipeline_mssql2psql_ingestion import job_mssql2psql_ingestion

daily_pipeline_mssql2psql_ingestion = build_schedule_from_partitioned_job(job_mssql2psql_ingestion)
