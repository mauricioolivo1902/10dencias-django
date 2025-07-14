# Generated manually for updating product descriptions to emphasize Ecuadorian origin

from django.db import migrations

def update_ecuadorian_descriptions(apps, schema_editor):
    # Obtenemos el modelo Producto
    Producto = apps.get_model('store', 'Producto')

    # Diccionario con las descripciones actualizadas enfatizando origen ecuatoriano
    descripciones_ecuatorianas = {
        "Taza Inspiradora": "Taza de cerámica 100% ecuatoriana, elaborada artesanalmente con materiales de la más alta calidad. Cada mañana será una nueva oportunidad para brillar con frases motivacionales que te recordarán tu potencial.",
        "Camiseta Motivacional": "Camiseta 100% algodón ecuatoriano, confeccionada con técnicas tradicionales y modernas. Lleva tu actitud positiva a todas partes con mensajes inspiradores que te motivarán a perseguir tus sueños.",
        "Hoodie con Actitud": "Hoodie 100% ecuatoriano, confeccionado con materiales premium y técnicas artesanales. Abrigo y motivación en uno solo, perfecto para días fríos y momentos de reflexión con frases que te recordarán tu potencial ilimitado.",
        "Gorra de Metas": "Gorra 100% ecuatoriana, elaborada con técnicas artesanales y materiales de primera calidad. Protege tu cabeza y tu determinación con mensajes motivacionales que te acompañarán en cada paso hacia el éxito.",
        "Medias Inspiradoras": "Medias 100% ecuatorianas, tejidas artesanalmente con algodón premium. Paso a paso hacia tus sueños con frases que te motivarán desde el primer paso del día, combinando estilo y comodidad perfectamente.",
        "Agenda de Metas": "Agenda 100% ecuatoriana, elaborada con papel reciclado y técnicas artesanales. Organiza tus sueños y hazlos realidad con secciones especiales para planificar tus metas y celebrar logros.",
        "Bolso Motivacional": "Bolso 100% ecuatoriano, confeccionado artesanalmente con materiales sostenibles. Lleva tus cosas y tu determinación con mensajes que te recordarán tu capacidad de lograr cualquier cosa que te propongas.",
        "Termo Inspirador": "Termo 100% ecuatoriano, elaborado con acero inoxidable de la más alta calidad. Mantén tu energía y tu motivación con tecnología que preserva la temperatura mientras te recuerda que eres capaz de grandes cosas.",
        "Maceta de Crecimiento": "Maceta 100% ecuatoriana, elaborada artesanalmente con arcilla natural. Haz crecer tus plantas y tus sueños con mensajes motivacionales que te inspirarán mientras cuidas de tus plantas y de tus metas personales.",
        "Mochila de Sueños": "Mochila 100% ecuatoriana, confeccionada artesanalmente con materiales resistentes y sostenibles. Lleva tus sueños a donde vayas con compartimentos organizados y mensajes que te recordarán que el viaje hacia tus metas es tan importante como el destino."
    }

    # Actualizar cada producto con su nueva descripción ecuatoriana
    for nombre, descripcion in descripciones_ecuatorianas.items():
        try:
            producto = Producto.objects.get(nombre=nombre)
            producto.descripcion = descripcion
            producto.save()
        except Producto.DoesNotExist:
            print(f"Producto '{nombre}' no encontrado")

def reverse_update_ecuadorian_descriptions(apps, schema_editor):
    # Función para revertir la migración (opcional)
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_update_product_descriptions'),
    ]

    operations = [
        migrations.RunPython(update_ecuadorian_descriptions, reverse_update_ecuadorian_descriptions),
    ] 