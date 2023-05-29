dev:
	poetry run python manage.py runserver 0.0.0.0:5000

run:
	@ echo Runnig the production apllication
	poetry run sh scripts/entrypoint.sh

clear:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	rm -f ./.coverage
	rm -r htmlcov dist .pytest_cache staticfiles/statics
	find . -type f -name "*.sqlite3_*" -delete

.PHONE: run

statics:
	poetry run python manage.py collectstatic --no-input --clear

lint:
	@echo "Linting"
	poetry run black . --check
	flake8 igreja

format:
	@echo "Formating"
	poetry run isort .
	poetry run black .

tests:
	poetry run python manage.py test -v 2

poetry_export:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

poetry_config:
	poetry config virtualenvs.in-project true
