from dagster import repository
from dbt_spotify import dbt_spotify_job_sensor


@repository
def spotify_dbt_analytics():
    return [dbt_spotify_job_sensor]
