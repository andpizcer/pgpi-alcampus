#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collecstatic --noinput
python manage.py makemigrations
python manage.py migrate