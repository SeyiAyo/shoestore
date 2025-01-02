"""
WSGI config for shoestore project.

It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoestore.settings')

# This is the WSGI application variable that Vercel looks for
app = application = get_wsgi_application()
