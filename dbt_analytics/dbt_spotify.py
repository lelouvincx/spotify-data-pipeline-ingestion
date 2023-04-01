import os

from dagster import DefaultSensorStatus, op, job, asset_sensor, RunRequest, AssetKey
from dagster_dbt import dbt_cli_resource, dbt_run_op, dbt_test_op


my_dbt_resource = dbt_cli_resource.configured(
    {
        "project_dir": os.path.join("spotify"),
        "profiles_dir": os.path.join("."),
    }
)
run_dbt_spotify = dbt_run_op.alias(name="run_dbt_spotify")
test_dbt_spotify = dbt_test_op.alias(name="test_dbt_spotify")


@op
def init_dbt():
    return True


@job(resource_defs={"dbt": my_dbt_resource})
def dbt_spotify_job():
    init_step = init_dbt()
    analytics = run_dbt_spotify(init_step)
    test_dbt_spotify(analytics)


@asset_sensor(asset_key=AssetKey("trigger_dbt_spotify"), job=dbt_spotify_job)
def dbt_spotify_job_sensor(context, asset_event):
    yield RunRequest(run_key=context.cursor)
