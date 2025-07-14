"""
VISTAS DE LA APLICACIÓN STORE - 10TENDENCIAS
============================================

Este archivo contiene todas las vistas (views) de Django que manejan la lógica de negocio
de la tienda online "10tendencias". Cada vista es responsable de procesar las peticiones
HTTP y devolver las respuestas correspondientes.

ESTRUCTURA GENERAL:
- Vistas de catálogo y productos
- Vistas de carrito de compras
- Vistas de checkout y pedidos
- Vistas de API para formularios dinámicos
"""

from django.shortcuts import render, get_object_or_404
from .models import Pedido, Producto, FraseMotivacional
from .forms import CheckoutForm
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Provincia, Ciudad 
from .services import OrderService

# ============================================================================
# VISTAS DEL CATÁLOGO Y PRODUCTOS
# ============================================================================

def catalogo(request):
    """
    VISTA PRINCIPAL DEL CATÁLOGO
    -----------------------------
    
    Función: Muestra la página principal con todos los productos disponibles
    Método HTTP: GET
    Template: store/catalogo.html
    
    Lógica:
    1. Obtiene todos los productos de la base de datos
    2. Los pasa al template para renderizar la página del catálogo
    3. No requiere autenticación - es pública
    
    Contexto enviado al template:
    - productos: QuerySet con todos los productos
    """
    productos = Producto.objects.all()
    return render(request, 'store/catalogo.html', {'productos': productos})

def producto_detalle(request, producto_id):
    """
    VISTA DE DETALLE DE PRODUCTO
    -----------------------------
    
    Función: Muestra la página detallada de un producto específico
    Método HTTP: GET, POST
    Template: store/producto_detalle.html
    Parámetros: producto_id (ID del producto a mostrar)
    
    Lógica:
    1. GET: Muestra el producto con sus frases motivacionales disponibles
    2. POST: Procesa la selección de frase y redirige al checkout
    
    Flujo de trabajo:
    - Si es POST y se selecciona una frase:
        * Guarda la selección en la sesión del usuario
        * Redirige al checkout
    - Si es GET: Solo muestra la página
    
    Contexto enviado al template:
    - producto: Objeto Producto específico
    - frases: QuerySet con todas las frases motivacionales
    """
    producto = get_object_or_404(Producto, pk=producto_id)
    frases = FraseMotivacional.objects.all()

    # Procesamiento de formulario POST (selección de frase)
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

    # Renderizado normal (GET)
    contexto = {
        'producto': producto,
        'frases': frases
    }
    return render(request, 'store/producto_detalle.html', contexto)

# ============================================================================
# VISTAS DEL CARRITO DE COMPRAS
# ============================================================================

def add_to_cart(request, producto_id):
    """
    VISTA PARA AÑADIR PRODUCTOS AL CARRITO
    --------------------------------------
    
    Función: Añade un producto con frase personalizada al carrito
    Método HTTP: POST
    Parámetros: producto_id (ID del producto a añadir)
    
    Lógica:
    1. Obtiene el producto y la frase seleccionada
    2. Crea un identificador único para el item (producto + frase)
    3. Si el item ya existe, incrementa la cantidad
    4. Si es nuevo, lo añade al carrito
    5. Guarda el carrito en la sesión del usuario
    
    Estructura del carrito en sesión:
    {
        'item_id': {
            'producto_id': int,
            'producto_nombre': str,
            'producto_precio': str,
            'producto_imagen': str,
            'frase_id': int,
            'frase_texto': str,
            'cantidad': int
        }
    }
    """
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        frase_id = request.POST.get('frase_seleccionada')
        if not frase_id:
            return redirect('producto_detalle', producto_id=producto_id)
        
        # Obtenemos el objeto de la frase para acceder a su texto
        frase = get_object_or_404(FraseMotivacional, pk=frase_id)

        cart = request.session.get('cart', {})
        # Crear ID único combinando producto y frase
        item_id = f"{producto_id}-{frase_id}"

        if item_id in cart:
            # Si ya existe, incrementar cantidad
            cart[item_id]['cantidad'] += 1
        else:
            # Si es nuevo, añadirlo al carrito
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
    """
    VISTA DEL CARRITO DE COMPRAS
    -----------------------------
    
    Función: Muestra el contenido actual del carrito
    Método HTTP: GET
    Template: store/cart_detail.html
    
    Lógica:
    1. Obtiene el carrito de la sesión del usuario
    2. Calcula subtotales y total general
    3. Renderiza la página del carrito
    
    Cálculos realizados:
    - Precio por item (convertido a float)
    - Subtotal por item (precio × cantidad)
    - Total del carrito (suma de todos los subtotales)
    """
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
    """
    VISTA PARA ELIMINAR PRODUCTOS DEL CARRITO
    -----------------------------------------
    
    Función: Elimina un item específico del carrito
    Método HTTP: GET
    Parámetros: item_id (ID único del item a eliminar)
    
    Lógica:
    1. Obtiene el carrito de la sesión
    2. Elimina el item especificado
    3. Guarda el carrito actualizado
    4. Redirige de vuelta al carrito
    
    Nota: Esta vista no requiere confirmación, elimina directamente
    """
    cart = request.session.get('cart', {})
    
    # Si el item_id existe en el carrito, lo eliminamos
    if item_id in cart:
        del cart[item_id]
        # Guardamos la versión actualizada del carrito en la sesión
        request.session['cart'] = cart
        
    return redirect('cart_detail')

# ============================================================================
# VISTAS DE CHECKOUT Y PEDIDOS
# ============================================================================

def checkout_view(request):
    """
    VISTA DEL CHECKOUT (FINALIZAR COMPRA)
    -------------------------------------
    
    Función: Maneja el proceso de finalización de compra
    Método HTTP: GET, POST
    Template: store/checkout.html
    
    Lógica:
    1. GET: Muestra el formulario de checkout con resumen del carrito
    2. POST: Procesa el formulario y crea el pedido
    
    Validaciones:
    - Verifica que el carrito no esté vacío
    - Valida el formulario de datos de facturación
    - Maneja errores en la creación del pedido
    
    Flujo de éxito:
    1. Formulario válido → Crea pedido usando OrderService
    2. Limpia el carrito de la sesión
    3. Redirige a página de pedido exitoso
    
    Contexto enviado al template:
    - form: Formulario de checkout
    - cart: Items del carrito con cálculos
    - cart_total: Total de la compra
    """
    # Verificar que el carrito no esté vacío
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('catalogo')

    # Calcular precios y totales
    for item in cart.values():
        item['precio'] = float(item['producto_precio'])
        item['subtotal'] = item['precio'] * item['cantidad']
    
    cart_total = sum(item['subtotal'] for item in cart.values())

    # Procesar formulario POST
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                # Crear pedido usando el servicio
                pedido = OrderService.create_order(form.cleaned_data, cart)
                
                # Limpiar carrito de la sesión
                del request.session['cart']
                
                # Redirigir a página de éxito
                return redirect('pedido_exitoso', pedido_id=pedido.id)
                
            except Exception as e:
                print(f"Error al crear el pedido: {e}")
    else:
        form = CheckoutForm()

    contexto = {
        'form': form,
        'cart': cart,
        'cart_total': cart_total
    }
    return render(request, 'store/checkout.html', contexto)

def pedido_exitoso(request, pedido_id):
    """
    VISTA DE PEDIDO EXITOSO
    ------------------------
    
    Función: Muestra la confirmación de pedido exitoso
    Método HTTP: GET
    Template: store/pedido_exitoso.html
    Parámetros: pedido_id (ID del pedido creado)
    
    Lógica:
    1. Obtiene el pedido específico de la base de datos
    2. Muestra la página de confirmación con detalles del pedido
    
    Seguridad:
    - Usa get_object_or_404 para evitar acceso a pedidos inexistentes
    - No requiere autenticación (acceso público por URL)
    
    Contexto enviado al template:
    - pedido: Objeto Pedido con todos sus datos relacionados
    """
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    contexto = {
        'pedido': pedido
    }
    return render(request, 'store/pedido_exitoso.html', contexto)

# ============================================================================
# VISTAS DE API (AJAX)
# ============================================================================

def get_provincias(request):
    """
    API PARA OBTENER PROVINCIAS
    ---------------------------
    
    Función: Devuelve las provincias de un país en formato JSON
    Método HTTP: GET
    Parámetros: pais_id (ID del país)
    Respuesta: JSON con lista de provincias
    
    Uso: Llamada por AJAX desde el formulario de checkout
    cuando se selecciona un país diferente
    
    Estructura de respuesta:
    [
        {"id": 1, "nombre": "Azuay"},
        {"id": 2, "nombre": "Bolívar"},
        ...
    ]
    """
    pais_id = request.GET.get('pais_id')
    provincias = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')
    data = list(provincias.values('id', 'nombre'))
    return JsonResponse(data, safe=False)

def get_ciudades(request):
    """
    API PARA OBTENER CIUDADES
    -------------------------
    
    Función: Devuelve las ciudades de una provincia en formato JSON
    Método HTTP: GET
    Parámetros: provincia_id (ID de la provincia)
    Respuesta: JSON con lista de ciudades
    
    Uso: Llamada por AJAX desde el formulario de checkout
    cuando se selecciona una provincia diferente
    
    Estructura de respuesta:
    [
        {"id": 1, "nombre": "Cuenca"},
        {"id": 2, "nombre": "Gualaceo"},
        ...
    ]
    """
    provincia_id = request.GET.get('provincia_id')
    ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
    data = list(ciudades.values('id', 'nombre'))
    return JsonResponse(data, safe=False)

# ============================================================================
# NOTAS IMPORTANTES SOBRE LA ARQUITECTURA
# ============================================================================

"""
ARQUITECTURA Y PATRONES UTILIZADOS:

1. SEPARACIÓN DE RESPONSABILIDADES:
   - Vistas: Manejan la lógica de presentación y navegación
   - Servicios: Manejan la lógica de negocio compleja (OrderService)
   - Modelos: Manejan la estructura de datos
   - Forms: Manejan la validación de formularios

2. GESTIÓN DE SESIONES:
   - El carrito se almacena en request.session
   - Permite persistencia entre páginas sin base de datos
   - Se limpia automáticamente al completar el pedido

3. MANEJO DE ERRORES:
   - get_object_or_404 para objetos inexistentes
   - Try-catch en operaciones críticas (creación de pedidos)
   - Redirecciones apropiadas en caso de error

4. SEGURIDAD:
   - Validación de formularios con Django Forms
   - Sanitización de datos de entrada
   - Protección contra acceso a recursos inexistentes

5. UX/UI:
   - Redirecciones lógicas en el flujo de compra
   - Feedback inmediato al usuario
   - URLs amigables y descriptivas

6. ESCALABILIDAD:
   - Código modular y reutilizable
   - Separación clara entre lógica de negocio y presentación
   - APIs RESTful para funcionalidades dinámicas
""" 