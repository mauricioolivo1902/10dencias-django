# Patrón: Modelo (M de MTV/MVC)
# Define la estructura de los datos y la lógica asociada a cada entidad.
# Repository: El ORM de Django actúa como repositorio para acceder a los datos.
from django.db import models

# Modelo para los países
class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para las provincias, relacionado con un País
class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    # Clave foránea: Cada provincia pertenece a un único país.
    # on_delete=models.CASCADE significa que si un país es eliminado,
    # todas sus provincias también lo serán.
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo para las ciudades, relacionado con una Provincia
class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    # Clave foránea: Cada ciudad pertenece a una única provincia.
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombre}, {self.provincia.nombre}'

# Modelo para las frases motivacionales
class FraseMotivacional(models.Model):
    # Usamos TextField porque una frase puede ser más larga que un CharField.
    texto = models.TextField()
    destacada = models.BooleanField(default=False, help_text="Marcar si la frase debe mostrarse en la web (máximo 3)")

    def __str__(self):
        return self.texto[:50] # Muestra los primeros 50 caracteres en el admin

# Modelo para los productos del catálogo
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    # Usamos DecimalField para precios para evitar problemas de redondeo con float.
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Para la imagen, por ahora guardaremos la URL. Más adelante podríamos implementar la subida de archivos.
    url_imagen = models.URLField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)  # Nuevo campo
    
    def __str__(self):
        return self.nombre

class Cupon(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de descuento, ej: 10 para 10%")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} ({self.descuento_porcentaje}%)"

# Modelo para la información general del pedido
class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    # Campos para cupón y descuento
    cupon_aplicado = models.ForeignKey(Cupon, on_delete=models.SET_NULL, null=True, blank=True)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Pedido #{self.id} - {self.fecha_pedido.strftime("%Y-%m-%d")}'

    @property
    def total(self):
        # Calcula el total sumando los subtotales de cada detalle del pedido
        detalles = self.detallepedido_set.all()
        total = sum([item.subtotal for item in detalles])
        return total
    
    @property
    def total_con_descuento(self):
        # Calcula el total con descuento aplicado
        return self.total - self.descuento_aplicado

# Modelo para cada item dentro de un pedido
class DetallePedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    frase_personalizada = models.ForeignKey(FraseMotivacional, on_delete=models.SET_NULL, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.producto.nombre} para Pedido #{self.pedido.id}'
    
    @property
    def subtotal(self):
        # El subtotal es el precio del producto por la cantidad
        return self.producto.precio * self.cantidad

# Modelo para los datos de facturación asociados a un pedido
class DatosFacturacion(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    numero_identificacion = models.CharField(max_length=20) # Guardamos como Char para flexibilidad
    
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    direccion_linea_1 = models.CharField(max_length=200)

    def __str__(self):
        return f'Datos de facturación para Pedido #{self.pedido.id}'