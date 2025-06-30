def cart_context(request):
    cart = request.session.get('cart', {})
    item_count = sum(item['cantidad'] for item in cart.values())
    return {'cart_item_count': item_count}