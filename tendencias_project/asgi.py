# Patrón: ASGI (Asynchronous Server Gateway Interface)
# Este archivo permite que el proyecto Django sea ejecutado en servidores asíncronos.
# Facilita la escalabilidad y el soporte para WebSockets y tareas en tiempo real.
"""
ASGI config for tendencias_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tendencias_project.settings')

application = get_asgi_application()
