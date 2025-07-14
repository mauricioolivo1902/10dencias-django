from django.shortcuts import render, get_object_or_404
from .models import Pedido, Producto, FraseMotivacional, Cupon
from .forms import CheckoutForm
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Provincia, Ciudad 
from .services import PedidoService

# Patrón: MTV (Modelo-Template-Vista, variante de MVC)

# Vista para la página del catálogo
def catalogo(request):
    # Muestra todos los productos disponibles en el catálogo.
    productos = Producto.objects.all()
    return render(request, 'store/catalogo.html', {'productos': productos})

def producto_detalle(request, producto_id):
    # Muestra el detalle de un producto y permite seleccionar una frase personalizada.
    producto = get_object_or_404(Producto, pk=producto_id)
    frases = FraseMotivacional.objects.filter(destacada=True)

    # Si el usuario envía el formulario, guarda la selección en la sesión y redirige al checkout.
    if request.method == 'POST':
        frase_id = request.POST.get('frase_seleccionada')
        if frase_id:
            request.session['pedido_actual'] = {
                'producto_id': producto.id,
                'frase_id': int(frase_id),
            }
            return redirect('checkout')
    contexto = {
        'producto': producto,
        'frases': frases
    }
    return render(request, 'store/producto_detalle.html', contexto)
    
    # Renderizamos la nueva plantilla 'producto_detalle.html' con el contexto.
    return render(request, 'store/producto_detalle.html', contexto)

def checkout_view(request):
    # Gestiona el proceso de compra: muestra el carrito, aplica cupones y finaliza el pedido.
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('catalogo')
    for item in cart.values():
        item['precio'] = float(item['producto_precio'])
        item['subtotal'] = item['precio'] * item['cantidad']
    cart_total = sum(item['subtotal'] for item in cart.values())
    descuento = 0
    cupon_aplicado = None
    cupon_error = None
    cupon_codigo = ''
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        cupon_codigo = request.POST.get('cupon', '').strip()
        if 'aplicar_cupon' in request.POST:
            # Aplica el cupón si es válido y calcula el descuento.
            if cupon_codigo:
                try:
                    cupon = Cupon.objects.get(codigo__iexact=cupon_codigo, activo=True)
                    descuento = (cart_total * float(cupon.descuento_porcentaje)) / 100
                    cupon_aplicado = cupon
                except Cupon.DoesNotExist:
                    cupon_error = 'Cupón inválido o inactivo.'
        elif 'finalizar_compra' in request.POST:
            # Finaliza la compra, valida el cupón y crea el pedido.
            if cupon_codigo:
                try:
                    cupon = Cupon.objects.get(codigo__iexact=cupon_codigo, activo=True)
                    descuento = (cart_total * float(cupon.descuento_porcentaje)) / 100
                    cupon_aplicado = cupon
                except Cupon.DoesNotExist:
                    cupon_error = 'Cupón inválido o inactivo.'
            if form.is_valid():
                try:
                    pedido_service = PedidoService()
                    pedido = pedido_service.crear_pedido(
                        form.cleaned_data, 
                        cart, 
                        cupon_aplicado=cupon_aplicado,
                        descuento_aplicado=descuento
                    )
                    del request.session['cart']
                    return redirect('pedido_exitoso', pedido_id=pedido.id)
                except Exception as e:
                    print(f"Error al crear el pedido: {e}")
    else:
        form = CheckoutForm()
    total_final = cart_total - descuento
    contexto = {
        'form': form,
        'cart': cart,
        'cart_total': cart_total,
        'descuento': descuento,
        'cupon_aplicado': cupon_aplicado,
        'cupon_error': cupon_error,
        'total_final': total_final
    }
    return render(request, 'store/checkout.html', contexto)

def get_provincias(request):
    # Devuelve las provincias de un país específico en formato JSON para AJAX.
    pais_id = request.GET.get('pais_id')
    provincias = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')
    data = list(provincias.values('id', 'nombre'))
    return JsonResponse(data, safe=False)


def get_ciudades(request):
    # Devuelve las ciudades de una provincia específica en formato JSON para AJAX.
    provincia_id = request.GET.get('provincia_id')
    ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
    data = list(ciudades.values('id', 'nombre'))
    return JsonResponse(data, safe=False)

def add_to_cart(request, producto_id):
    # Añade un producto y frase personalizada al carrito de la sesión.
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        frase_id = request.POST.get('frase_seleccionada')
        if not frase_id:
            return redirect('producto_detalle', producto_id=producto_id)
        frase = get_object_or_404(FraseMotivacional, pk=frase_id)
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
                'frase_texto': frase.texto,
                'cantidad': 1,
            }
        request.session['cart'] = cart
        return redirect('catalogo')
    return redirect('producto_detalle', producto_id=producto_id)

def cart_detail(request):
    # Muestra el detalle del carrito con los productos añadidos y el total.
    cart = request.session.get('cart', {})
    for item in cart.values():
        item['precio'] = float(item['producto_precio'])
        item['subtotal'] = item['precio'] * item['cantidad']
    cart_total = sum(item['subtotal'] for item in cart.values())
    contexto = {
        'cart': cart,
        'cart_total': cart_total
    }
    return render(request, 'store/cart_detail.html', contexto)

def remove_from_cart(request, item_id):
    # Elimina un producto del carrito de la sesión.
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
    return redirect('cart_detail')

def pedido_exitoso(request, pedido_id):
    # Muestra la página de confirmación de pedido exitoso con detalles del pedido.
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    contexto = {
        'pedido': pedido,
        'tiene_cupon': pedido.cupon_aplicado is not None,
        'cupon': pedido.cupon_aplicado,
        'descuento': pedido.descuento_aplicado,
        'total_con_descuento': pedido.total_con_descuento
    }
    return render(request, 'store/pedido_exitoso.html', contexto)