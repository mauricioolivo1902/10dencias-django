from django.db import transaction
from .models import Pedido, DetallePedido, DatosFacturacion, Producto, FraseMotivacional

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(form_data, cart_data): # Cambiamos el nombre del parámetro a cart_data
        """
        Crea un pedido completo a partir del carrito de compras.
        :param form_data: Diccionario con los datos limpios del CheckoutForm.
        :param cart_data: El diccionario del carrito desde la sesión.
        :return: El objeto Pedido creado.
        """
        # 1. Crear el objeto Pedido principal (sin cambios)
        pedido = Pedido.objects.create()

        # 2. Crear los Datos de Facturación asociados (sin cambios)
        DatosFacturacion.objects.create(
            pedido=pedido,
            nombre=form_data['nombre'],
            apellido=form_data['apellido'],
            numero_identificacion=form_data['numero_identificacion'],
            pais=form_data['pais'],
            provincia=form_data['provincia'],
            ciudad=form_data['ciudad'],
            direccion_linea_1=form_data['direccion_linea_1']
        )

        # 3. Crear los Detalles del Pedido (lógica actualizada)
        # Iteramos sobre cada ítem en los datos del carrito
        for item_id, item_data in cart_data.items():
            try:
                # Obtenemos los objetos Producto y Frase desde la BD
                producto = Producto.objects.get(pk=item_data['producto_id'])
                frase = FraseMotivacional.objects.get(pk=item_data['frase_id'])
                
                # Creamos un DetallePedido para este ítem
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    frase_personalizada=frase,
                    cantidad=item_data['cantidad']
                )
            except (Producto.DoesNotExist, FraseMotivacional.DoesNotExist) as e:
                # Si por alguna razón un producto o frase fue eliminado mientras estaba
                # en el carrito del usuario, lanzamos un error para detener la transacción.
                print(f"Error: No se encontró el producto o frase para el ítem {item_id}. Error: {e}")
                # Esto hará que la transacción atómica falle y no se cree el pedido.
                raise ValueError(f"Ítem del carrito no válido: {item_id}")
        
        return pedido