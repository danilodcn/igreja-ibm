clear:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	rm -f ./.coverage

.PHONE: run
dev:
	./.docker/development/entrypoint.sh

run:
	@ echo Runnig the production apllication
	./.docker/production/entrypoint.sh

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
