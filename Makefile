dev:
	newrelic-admin run-program ./manage.py runserver 0.0.0.0:5000

run:
	@ echo Runnig the production apllication
	newrelic-admin run-program gunicorn igreja.wsgi

clear:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	rm -f ./.coverage

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

poetry__config:
	poetry config virtualenvs.in-project true
