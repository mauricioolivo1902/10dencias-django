# Archivo de migración
# Permite actualizar las descripciones de los productos en la base de datos.

from django.db import migrations

def update_product_descriptions(apps, schema_editor):
    # Obtenemos el modelo Producto
    Producto = apps.get_model('store', 'Producto')

    # Diccionario con las descripciones actualizadas para cada producto
    descripciones = {
        "Taza Inspiradora": "Comienza cada mañana con energía positiva. Taza de cerámica de alta calidad con frases motivacionales que te recordarán que cada día es una nueva oportunidad para brillar.",
        "Camiseta Motivacional": "Lleva tu actitud positiva a todas partes. Camiseta 100% algodón con mensajes inspiradores que te motivarán a perseguir tus sueños sin importar los obstáculos.",
        "Hoodie con Actitud": "Abrigo y motivación en uno solo. Hoodie cómodo y moderno con frases que te recordarán tu potencial ilimitado. Perfecto para días fríos y momentos de reflexión.",
        "Gorra de Metas": "Protege tu cabeza y tu determinación. Gorra casual con mensajes motivacionales que te acompañarán en cada paso hacia el éxito. Diseño versátil para cualquier ocasión.",
        "Medias Inspiradoras": "Paso a paso hacia tus sueños. Medias cómodas y duraderas con frases que te motivarán desde el primer paso del día. Combinan estilo y comodidad perfectamente.",
        "Agenda de Metas": "Organiza tus sueños y hazlos realidad. Agenda de alta calidad con secciones especiales para planificar tus metas, celebrar logros y mantener el enfoque en lo que realmente importa.",
        "Bolso Motivacional": "Lleva tus cosas y tu determinación. Bolso espacioso y resistente con mensajes que te recordarán tu capacidad de lograr cualquier cosa que te propongas.",
        "Termo Inspirador": "Mantén tu energía y tu motivación. Termo de acero inoxidable que mantiene tus bebidas a la temperatura perfecta mientras te recuerda que eres capaz de grandes cosas.",
        "Maceta de Crecimiento": "Haz crecer tus plantas y tus sueños. Maceta decorativa con mensajes motivacionales que te inspirarán mientras cuidas de tus plantas y de tus metas personales.",
        "Mochila de Sueños": "Lleva tus sueños a donde vayas. Mochila resistente y espaciosa con compartimentos organizados y mensajes que te recordarán que el viaje hacia tus metas es tan importante como el destino."
    }

    # Actualizar cada producto con su nueva descripción
    for nombre, descripcion in descripciones.items():
        try:
            producto = Producto.objects.get(nombre=nombre)
            producto.descripcion = descripcion
            producto.save()
        except Producto.DoesNotExist:
            print(f"Producto '{nombre}' no encontrado")

def reverse_update_descriptions(apps, schema_editor):
    # Función para revertir la migración (opcional)
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_producto_descripcion'),
    ]

    operations = [
        migrations.RunPython(update_product_descriptions, reverse_update_descriptions),
    ] 