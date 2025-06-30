from django.shortcuts import render, get_object_or_404
from .models import Pedido, Producto, FraseMotivacional
from .forms import CheckoutForm
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Provincia, Ciudad 
from .services import OrderService

# Vista para la página del catálogo (sin cambios)
def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'store/catalogo.html', {'productos': productos})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    frases = FraseMotivacional.objects.all()

    # Si el usuario envía el formulario (hace clic en el botón)
    if request.method == 'POST':
        frase_id = request.POST.get('frase_seleccionada')
        if frase_id:
            # Guardamos la selección en la sesión del usuario
            request.session['pedido_actual'] = {
                'producto_id': producto.id,
                'frase_id': int(frase_id),
            }
            # Redirigimos a la página de checkout
            return redirect('checkout')
        # (Aquí podría ir un mensaje de error si no se selecciona una frase)

    # Si es una petición GET, simplemente mostramos la página
    contexto = {
        'producto': producto,
        'frases': frases
    }
    return render(request, 'store/producto_detalle.html', contexto)
    
    # 4. Renderizamos la nueva plantilla 'producto_detalle.html' con el contexto.
    return render(request, 'store/producto_detalle.html', contexto)

def checkout_view(request):
    # Ahora leemos el carrito completo de la sesión
    cart = request.session.get('cart', {})
    if not cart:
        # Si el carrito está vacío, no hay nada que comprar.
        return redirect('catalogo')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
                    try:
                        # El servicio nos devuelve el pedido que acaba de crear
                        pedido = OrderService.create_order(form.cleaned_data, cart)
                        
                        del request.session['cart']
                        
                        # ¡AQUÍ ESTÁ EL CAMBIO!
                        # Redirigimos a la nueva página de éxito, pasando el ID del pedido.
                        return redirect('pedido_exitoso', pedido_id=pedido.id)
                        
                    except Exception as e:
                        print(f"Error al crear el pedido: {e}")
                
    else:
        form = CheckoutForm()

    contexto = {'form': form}
    return render(request, 'store/checkout.html', contexto)

def get_provincias(request):
    """
    Vista que devuelve las provincias de un país específico en formato JSON.
    Es llamada por el script de AJAX cuando se selecciona un país.
    """
    # Obtenemos el ID del país desde los parámetros GET de la petición
    pais_id = request.GET.get('pais_id')
    # Filtramos las provincias que pertenecen a ese país
    provincias = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')
    # Convertimos el queryset a una lista de diccionarios para poder serializarla a JSON
    # El campo 'id' es el value del <option> y 'nombre' es el texto visible.
    data = list(provincias.values('id', 'nombre'))
    return JsonResponse(data, safe=False)


def get_ciudades(request):
    """
    Vista que devuelve las ciudades de una provincia específica en formato JSON.
    """
    provincia_id = request.GET.get('provincia_id')
    ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
    data = list(ciudades.values('id', 'nombre'))
    return JsonResponse(data, safe=False)

def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        frase_id = request.POST.get('frase_seleccionada')
        if not frase_id:
            return redirect('producto_detalle', producto_id=producto_id)
        
        # Obtenemos el objeto de la frase para acceder a su texto
        frase = get_object_or_404(FraseMotivacional, pk=frase_id) # <-- LÍNEA AÑADIDA

        cart = request.session.get('cart', {})
        item_id = f"{producto_id}-{frase_id}"

        if item_id in cart:
            cart[item_id]['cantidad'] += 1
        else:
            cart[item_id] = {
                'producto_id': producto_id,
                'producto_nombre': producto.nombre,
                'producto_precio': str(producto.precio),
                'producto_imagen': producto.url_imagen,
                'frase_id': int(frase_id),
                'frase_texto': frase.texto, # <-- LÍNEA AÑADIDA
                'cantidad': 1,
            }
        
        request.session['cart'] = cart
        return redirect('catalogo')
    return redirect('producto_detalle', producto_id=producto_id)

def cart_detail(request):
    cart = request.session.get('cart', {})
    # Convertimos el precio a float y calculamos el subtotal para cada ítem
    for item in cart.values():
        item['precio'] = float(item['producto_precio'])
        item['subtotal'] = item['precio'] * item['cantidad']
    
    # Calculamos el total del carrito
    cart_total = sum(item['subtotal'] for item in cart.values())

    contexto = {
        'cart': cart,
        'cart_total': cart_total
    }
    return render(request, 'store/cart_detail.html', contexto)

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    
    # Si el item_id existe en el carrito, lo eliminamos
    if item_id in cart:
        del cart[item_id]
        # Guardamos la versión actualizada del carrito en la sesión
        request.session['cart'] = cart
        
    return redirect('cart_detail')

def pedido_exitoso(request, pedido_id):
    # Usamos get_object_or_404 para asegurarnos de que el pedido exista
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    contexto = {
        'pedido': pedido
    }
    return render(request, 'store/pedido_exitoso.html', contexto)