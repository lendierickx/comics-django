"""
WSGI config for ecantina_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecantina_project.settings")

# When the application loads for the first time, clear the previous cache.
from django.core.cache import caches
try:
    cache = caches['default']
    if cache is not None:
        cache.clear()
        print("Cache Cleared")
except Exception as e:
    print(e)

application = get_wsgi_application()
