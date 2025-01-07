import os
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Create static directories
static_dirs = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'staticfiles'),
]

# Create directories if they don't exist
for directory in static_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")
