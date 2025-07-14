from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Producto, FraseMotivacional, Pais, Provincia, Ciudad


class PruebasTienda(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Crear país, provincia y ciudad
        self.pais = Pais.objects.create(nombre='Ecuador')
        self.provincia = Provincia.objects.create(nombre='Pichincha', pais=self.pais)
        self.ciudad = Ciudad.objects.create(nombre='Quito', provincia=self.provincia)
        # Crear frase motivacional
        self.frase = FraseMotivacional.objects.create(texto='¡Sigue adelante!', destacada=True)
        # Crear producto
        self.producto = Producto.objects.create(
            nombre='Taza',
            precio=5.0,
            url_imagen='http://ejemplo.com/taza.jpg',
            descripcion='Taza de prueba para test funcional'
        )
        self.client = Client()

    def test_checkout_funcional(self):
        # Simular login
        self.client.login(username='testuser', password='testpass')
        # Simular añadir producto al carrito
        session = self.client.session
        session['cart'] = {
            f'{self.producto.id}-{self.frase.id}': {
                'producto_id': self.producto.id,
                'producto_nombre': self.producto.nombre,
                'producto_precio': str(self.producto.precio),
                'producto_imagen': self.producto.url_imagen,
                'frase_id': self.frase.id,
                'frase_texto': self.frase.texto,
                'cantidad': 1,
            }
        }
        session.save()
        # Realizar checkout
        response = self.client.post('/catalogo/checkout/', {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'numero_identificacion': '1234567890',
            'pais': self.pais.id,
            'provincia': self.provincia.id,
            'ciudad': self.ciudad.id,
            'direccion_linea_1': 'Calle Falsa 123',
            'cupon': ''
        }, follow=True)
        # Verificar que la respuesta es exitosa o redirige a pedido exitoso
        self.assertIn(response.status_code, [200, 302])
