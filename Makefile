.PHONY: test sample api

test:
	python -m unittest discover -s tests

sample:
	python -m packages.veyra_core.cli seeds/aceco_like_case.json

api:
	uvicorn apps.api.main:app --reload
