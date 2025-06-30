from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la página del catálogo (la que ya teníamos)
    path('', views.catalogo, name='catalogo'),
    
    # NUEVA RUTA: para la página de detalle de un producto
    # <int:producto_id> es un "capturador de ruta". Captura un número entero de la URL
    # y lo pasa a la vista como un argumento llamado 'producto_id'.
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('', views.catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    
    # NUEVA RUTA: para la página de checkout
    path('checkout/', views.checkout_view, name='checkout'),

    path('', views.catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('checkout/', views.checkout_view, name='checkout'),

    # NUEVAS RUTAS DE API: para obtener datos en formato JSON
    path('api/provincias/', views.get_provincias, name='get_provincias'),
    path('api/ciudades/', views.get_ciudades, name='get_ciudades'),

    path('add-to-cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),

    path('add-to-cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    # NUEVAS RUTAS PARA GESTIONAR EL CARRITO
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('remove-from-cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # NUEVA RUTA: para la página de pedido exitoso
    path('pedido-exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
]