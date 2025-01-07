import os
from pathlib import Path

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoestore.settings')
os.environ.setdefault('DJANGO_ENV', 'production')
os.environ.setdefault('STATIC_ROOT', '/tmp/static')
os.environ.setdefault('MEDIA_ROOT', '/tmp/media')

# Create runtime directories in /tmp
DIRS = ['static', 'media', 'logs']
for dir_name in DIRS:
    try:
        os.makedirs(os.path.join('/tmp', dir_name), exist_ok=True)
    except OSError:
        # If directory creation fails, continue anyway
        # The application will fall back to console logging
        pass

# Import Django WSGI handler
from shoestore.wsgi import application
app = application
