import os
from pathlib import Path

# Create necessary directories
BASE_DIR = Path(__file__).resolve().parent
DIRS = ['static', 'staticfiles', 'media', 'logs']
for dir_name in DIRS:
    os.makedirs(os.path.join(BASE_DIR, dir_name), exist_ok=True)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoestore.settings')
os.environ.setdefault('DJANGO_ENV', 'production')

# Import Django WSGI handler
from shoestore.wsgi import application
app = application
