include env

build:
	docker-compose build

up:
	docker-compose --env-file env up -d

down:
	docker-compose --env-file env down

restart:
	docker-compose --env-file env down && docker-compose --env-file env up -d

to_mysql:
	docker exec -it de_mysql mysql -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE}

mysql_create:
	docker exec -it de_mysql mysql --local_infile -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE} -e"source /tmp/mysql_datasource.sql"

mysql_load:
	docker exec -it de_mysql mysql --local_infile -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE} -e"source /tmp/mysql_load_csv.sql"

mysql_set_foreign_key:
	docker exec -it de_mysql mysql --local_infile -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE} -e"source /tmp/mysql_set_foreign_key.sql"

to_psql:
	docker exec -it de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

to_psql_no_db:
	docker exec -it de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/postgres

psql_create:
	docker exec -it de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/spotify -f /tmp/psql_datasource.sql -a

dbt_install_deps:
	docker exec -it dbt_analytics cd /opt/dagster/app/spotify && dbt deps

check:
	black ./elt_pipeline --check

lint:
	flake8 ./elt_pipeline

test:
	docker exec elt_pipeline python -m pytest -vv --cov=utils tests/utils \
	&& docker exec elt_pipeline python -m pytest -vv --cov=ops tests/ops
	
install:
	python3 -V \
	&& python3 -m venv venv \
	&& . venv/bin/activate \
	&& pip install --upgrade pip && pip install -r requirements.txt
