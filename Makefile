fmt:
	black src tests

test:
	pytest

watch-tests:
	find src tests -name "*.py" | entr pytest

