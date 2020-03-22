SOURCE_DIRECTORIES= km scripts tests app.py graphing.py constants.py

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

test:
	poetry run python -m pytest

run-app:
	poetry run streamlit run app.py
