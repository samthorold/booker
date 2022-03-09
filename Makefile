docs-serve:
	venv/bin/python -m mkdocs serve

docs-build:
	venv/bin/python -m mkdocs build

docs-watch:
	find src tests -name "*.py" | entr -r venv/bin/python -m mkdocs serve

docs-deploy:
	venv/bin/python -m mkdocs gh-deploy

fmt:
	venv/bin/python -m black src tests

fmt-watch:
	find src tests -name "*.py" | entr venv/bin/python -m black src

test:
	venv/bin/python -m pytest

test-watch:
	find src tests -name "*.py" | entr venv/bin/python -m pytest -v

type:
	venv/bin/python -m mypy src/

type-watch:
	find src tests -name "*.py" | entr venv/bin/python -m mypy src

