SOURCE_DIRECTORIES= km scripts tests streamlit_app app.py

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

test:
	poetry run python -m pytest

run-app:
	poetry run streamlit run app.py

start-flask-app:
	poetry run python -m km.flask_api.app
