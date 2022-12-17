run:
	dbt run --profiles-dir ./ --project-dir spotify

seed:
	dbt seed --profiles-dir ./ --project-dir spotify --full-refresh

docs:
	dbt docs generate --profiles-dir ./ --project-dir spotify \
		&& dbt docs serve --profiles-dir ./ --project-dir spotify

select:
	dbt run --profiles-dir ./ --project-dir spotify --select $(script)

test:
	dbt test --profiles-dir ./ --project-dir spotify
