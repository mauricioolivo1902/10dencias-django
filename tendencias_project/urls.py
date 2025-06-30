from django.contrib import admin
# ¡Asegúrate de importar 'include'!
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta línea le dice al proyecto que cualquier URL que empiece con 'catalogo/'
    # debe ser manejada por el archivo urls.py de nuestra app 'store'.
    path('catalogo/', include('store.urls')),
]