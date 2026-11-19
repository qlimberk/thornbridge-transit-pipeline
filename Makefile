.PHONY: setup skeleton test lint

setup:
	pip install -e ".[dev]"

skeleton:
	python -m src.ingest --months 2025-01
	python -m src.validate --months 2025-01

test:
	ruff check .
	pytest -v