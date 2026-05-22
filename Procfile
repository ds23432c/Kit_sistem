release: python manage.py migrate --no-input && python manage.py load_fixtures && gunicorn config.wsgi --workers 2 --bind 0.0.0.0:$PORT
web: gunicorn config.wsgi --workers 2 --bind 0.0.0.0:$PORT --log-file -
