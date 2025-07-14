from django.db import transaction
from .models import Pedido, DetallePedido, DatosFacturacion, Producto, FraseMotivacional

# Patrón: Service Layer (Capa de Servicios)
# Esta clase centraliza la lógica de negocio relacionada con pedidos.
# Principios SOLID: SRP (Responsabilidad Única) y OCP (Abierto/Cerrado)
class PedidoService:
    """
    Servicio para la creación de pedidos.
    SRP: Solo se encarga de la lógica de creación de pedidos.
    OCP: Se puede extender para cupones, descuentos, notificaciones, etc.
    """
    def crear_pedido(self, datos_facturacion, cart, cupon_aplicado=None, descuento_aplicado=0):
        # 1. Crear el pedido principal con información del cupón
        pedido = Pedido.objects.create(
            cupon_aplicado=cupon_aplicado,
            descuento_aplicado=descuento_aplicado
        )

        # 2. Crear los detalles del pedido
        for item in cart.values():
            producto = Producto.objects.get(pk=item['producto_id'])
            frase = FraseMotivacional.objects.get(pk=item['frase_id'])
            DetallePedido.objects.create(
                producto=producto,
                frase_personalizada=frase,
                pedido=pedido,
                cantidad=item['cantidad']
            )

        # 3. Crear los datos de facturación (solo los campos válidos, sin cupon)
        DatosFacturacion.objects.create(
            pedido=pedido,
            nombre=datos_facturacion['nombre'],
            apellido=datos_facturacion['apellido'],
            numero_identificacion=datos_facturacion['numero_identificacion'],
            pais=datos_facturacion['pais'],
            provincia=datos_facturacion['provincia'],
            ciudad=datos_facturacion['ciudad'],
            direccion_linea_1=datos_facturacion['direccion_linea_1']
        )
        return pedido

# OCP: Si quieres agregar lógica extra (descuentos, notificaciones, etc.),
# puedes crear una subclase que extienda PedidoService y sobreescriba crear_pedido.