.PHONY: run test

run: test
	uvicorn app.main:app --reload --port 8080

test:
	PYTHONPATH=. python -m pytest -v --tb=short