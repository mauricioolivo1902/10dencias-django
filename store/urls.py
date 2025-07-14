from django.urls import path
from . import views

urlpatterns = [
    # Rutas principales
    path('', views.catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    
    # Rutas del carrito
    path('add-to-cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Rutas de checkout y pedidos
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido-exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    
    # Rutas de API
    path('api/provincias/', views.get_provincias, name='get_provincias'),
    path('api/ciudades/', views.get_ciudades, name='get_ciudades'),
]