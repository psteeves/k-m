SOURCE_DIRECTORIES= km scripts tests

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black .

test:
	poetry run python -m pytest

start-app:
	poetry run python -m km.flask_api.app
