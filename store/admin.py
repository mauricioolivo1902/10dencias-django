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