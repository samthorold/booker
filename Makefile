docs-serve:
	venv/bin/python -m mkdocs serve

fmt:
	venv/bin/python -m black src tests

test:
	venv/bin/python -m pytest

watch-tests:
	find src tests -name "*.py" | entr venv/bin/python -m pytest

