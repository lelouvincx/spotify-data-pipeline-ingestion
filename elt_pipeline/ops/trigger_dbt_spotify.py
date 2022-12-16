from dagster import op, AssetMaterialization


@op
def trigger_dbt_spotify(context, upstream):
    context.log.info(f"Upstream status: {upstream}")
    context.log_event(
        AssetMaterialization(
            asset_key="trigger_dbt_spotify", description="Trigger job dbt spotify"
        )
    )
    return True
