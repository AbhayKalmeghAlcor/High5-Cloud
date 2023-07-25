"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODE = os.environ.get('MODE', 'devel')

if MODE == 'devel':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.devel')
elif MODE == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.staging')
elif MODE == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
else:
    raise ValueError(f"Invalid MODE environment variable: '{MODE}'")

application = get_wsgi_application()
