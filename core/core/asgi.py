"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
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

application = get_asgi_application()
