#!/bin/bash

# Exit on error
set -e

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p static staticfiles media logs

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput
