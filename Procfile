release: python manage.py migrate --no-input && python manage.py load_fixtures
web: gunicorn config.wsgi --workers 2 --bind 0.0.0.0:$PORT --log-file -
