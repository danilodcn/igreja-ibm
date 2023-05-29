
mkdir -p /app/staticfiles
python manage.py collectstatic --no-input

gunicorn -w 4 igreja.wsgi --bind 0.0.0.0:8000