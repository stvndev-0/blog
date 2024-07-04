release: python manage.py collectstatic --noinput
web: python manage.py migrate && gunicorn blog.wsgi