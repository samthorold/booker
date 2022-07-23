export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down img-build up

img-build: down
	docker-compose build

up:
	docker-compose up -d app

down:
	docker-compose down --remove-orphans

logs:
	docker-compose logs app | tail -100

docs-serve:
	venv/bin/python -m mkdocs serve

docs-build:
	venv/bin/python -m mkdocs build

docs-watch:
	venv/bin/python -m mkdocs serve

docs-deploy:
	venv/bin/python -m mkdocs gh-deploy

fmt:
	venv/bin/python -m black src tests

fmt-watch:
	find src tests -name "*.py" | entr venv/bin/python -m black src

test: up
	docker-compose run --rm --no-deps app sh -c "coverage run -m pytest /tests && coverage combine && coverage html --directory=/artefacts/htmlcov && coverage report -m --fail-under 100"

build-test: img-build up test

coverage:
	docker-compose run --rm --no-deps app sh -c "coverage combine && coverage report -m"

test-watch:
	find src tests -name "*.py" | entr venv/bin/python -m pytest -v

type:
	venv/bin/python -m mypy src/

type-watch:
	find src tests -name "*.py" | entr venv/bin/python -m mypy src

