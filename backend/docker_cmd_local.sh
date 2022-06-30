#!/usr/bin/env bash

python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000