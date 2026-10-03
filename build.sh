#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Load initial menu data (you have both initial_data.json and seed_data.json)
python manage.py loaddata initial_data.json

# Create admin superuser automatically on build
python manage.py createsuperuser --noinput || true