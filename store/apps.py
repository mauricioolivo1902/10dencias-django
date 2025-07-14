# Patrón: Configuración de Aplicaciones (Django AppConfig)
# Este archivo define la configuración de la app 'store'.
# Permite personalizar el comportamiento de la aplicación al iniciar el proyecto.
from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
