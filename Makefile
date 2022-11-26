include env

test:
	echo hello world

build:
	docker-compose build

build-test:
	docker-compose -f test-docker-compose.yml build

up:
	docker-compose --env-file env up -d

test-up:
	docker-compose -f test-docker-compose.yml --env-file env.test up -d

down:
	docker-compose --env-file env down

test-down:
	docker-compose -f test-docker-compose.yml --env-file env.test down

to_mysql:
	docker exec -it de_mysql mysql -uroot -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE}

to_psql:
	docker exec -ti de_psql psql postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

check:
	black ./elt_pipeline --check

lint:
	flake8 ./elt_pipeline

test-docker:
	docker exec elt_pipeline_test python -m pytest -vv --cov=utils tests/utils \
	&& docker exec elt_pipeline_test python -m pytest -vv --cov=ops tests/ops
	
install:
	python3 -V \
	&& python3 -m venv venv \
	&& . venv/bin/activate \
	&& pip install --upgrade pip && pip install -r requirements.txt
