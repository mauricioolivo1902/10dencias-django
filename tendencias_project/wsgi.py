# Patrón: WSGI (Web Server Gateway Interface)
# Este archivo permite que el proyecto Django sea ejecutado en servidores web tradicionales.
# Es el punto de entrada para servidores como Gunicorn, uWSGI, etc.
"""
WSGI config for tendencias_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tendencias_project.settings')

application = get_wsgi_application()
