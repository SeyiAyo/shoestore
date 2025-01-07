#!/bin/bash

echo "Starting build process..."

# Exit on error
set -e

echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p static staticfiles media logs

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Build process completed."
