# Archivo de migración
# Permite agregar productos faltantes a la base de datos.

from django.db import migrations

def add_missing_products(apps, schema_editor):
    # Obtenemos el modelo Producto
    Producto = apps.get_model('store', 'Producto')

    # Lista de los 6 productos faltantes
    productos_faltantes = [
        {
            "nombre": "Medias Inspiradoras",
            "precio": 8.50,
            "url_imagen": "https://via.placeholder.com/300x300.png?text=Medias",
            "descripcion": "Medias cómodas y motivacionales para empezar el día con energía."
        },
        {
            "nombre": "Agenda de Metas",
            "precio": 15.00,
            "url_imagen": "https://via.placeholder.com/300x300.png?text=Agenda",
            "descripcion": "Organiza tus sueños y metas con estilo y motivación."
        },
        {
            "nombre": "Bolso Motivacional",
            "precio": 35.00,
            "url_imagen": "https://via.placeholder.com/300x300.png?text=Bolso",
            "descripcion": "Lleva tus cosas y tu actitud positiva a todas partes."
        },
        {
            "nombre": "Termo Inspirador",
            "precio": 22.00,
            "url_imagen": "https://via.placeholder.com/300x300.png?text=Termo",
            "descripcion": "Mantén tu bebida favorita y tu motivación siempre contigo."
        },
        {
            "nombre": "Maceta de Crecimiento",
            "precio": 18.50,
            "url_imagen": "https://via.placeholder.com/300x300.png?text=Maceta",
            "descripcion": "Haz crecer tus plantas y tus sueños."
        },
        {
            "nombre": "Mochila de Sueños",
            "precio": 42.00,
            "url_imagen": "https://via.placeholder.com/300x300.png?text=Mochila",
            "descripcion": "Mochila espaciosa para llevar tus sueños a donde vayas."
        }
    ]

    # Crear cada producto si no existe
    for prod_data in productos_faltantes:
        Producto.objects.get_or_create(
            nombre=prod_data['nombre'],
            defaults=prod_data
        )

def reverse_add_missing_products(apps, schema_editor):
    # Función para revertir la migración (opcional)
    Producto = apps.get_model('store', 'Producto')
    
    productos_a_eliminar = [
        "Medias Inspiradoras",
        "Agenda de Metas", 
        "Bolso Motivacional",
        "Termo Inspirador",
        "Maceta de Crecimiento",
        "Mochila de Sueños"
    ]
    
    for nombre in productos_a_eliminar:
        Producto.objects.filter(nombre=nombre).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_pedido_detallepedido_datosfacturacion'),
    ]

    operations = [
        migrations.RunPython(add_missing_products, reverse_add_missing_products),
    ] 