#!/bin/bash

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
python -c "import os; [os.makedirs(d, exist_ok=True) for d in ['static', 'staticfiles', 'media', 'logs']]"

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput
