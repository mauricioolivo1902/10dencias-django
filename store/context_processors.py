# Patrón: Context Processor
# Este archivo define funciones que agregan variables globales al contexto de las plantillas.
# Permite compartir datos entre todas las vistas y plantillas de la app.
def cart_context(request):
    cart = request.session.get('cart', {})
    item_count = sum(item['cantidad'] for item in cart.values())
    return {'cart_item_count': item_count}