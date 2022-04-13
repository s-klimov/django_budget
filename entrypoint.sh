#!/usr/bin/env bash

./wait-for-it.sh db:5432 -- python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000