format: 
	poetry run isort -y
	poetry run black .

test:
	poetry run python -m pytest

start-app:
	poetry run python -m km.flask_api.app
