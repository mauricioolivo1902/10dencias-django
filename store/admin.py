# Patrón: Admin Site (Sitio de Administración)
# Este archivo registra los modelos para su gestión en el panel de administración de Django.
# Permite a los administradores gestionar los datos de la aplicación de forma sencilla.
from django.contrib import admin
from .models import Pais, Provincia, Ciudad, FraseMotivacional, Producto
from .models import Pedido, DetallePedido, DatosFacturacion

# Registramos cada modelo para que aparezca en el panel de administración.
# Django usará el método __str__ que definimos en los modelos para mostrar los objetos.
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Ciudad)
admin.site.register(FraseMotivacional)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(DatosFacturacion)

class FraseMotivacionalAdmin(admin.ModelAdmin):
    list_display = ('texto', 'destacada')
    list_filter = ('destacada',)
    search_fields = ('texto',)

admin.site.unregister(FraseMotivacional)
admin.site.register(FraseMotivacional, FraseMotivacionalAdmin)