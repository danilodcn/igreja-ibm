web: gunicorn igreja_ibm.wsgi
inicialize: python manage.py collectstatic --no-input && python manage.py migrate && python manage.py shell < igreja_ibm/scripts/create_user.py