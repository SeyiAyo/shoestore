#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    python3-dev \
    libpq-dev

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate
