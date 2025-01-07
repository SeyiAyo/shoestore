#!/bin/bash

# Install Python dependencies
pip install -r requirements-vercel.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (if needed)
python manage.py migrate --noinput
