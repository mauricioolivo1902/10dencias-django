# Archivo de migración
# Permite agregar las provincias de Ecuador a la base de datos.

from django.db import migrations

def add_ecuador_provinces(apps, schema_editor):
    # Obtenemos los modelos
    Pais = apps.get_model('store', 'Pais')
    Provincia = apps.get_model('store', 'Provincia')
    
    # Obtenemos Ecuador
    ecuador, created = Pais.objects.get_or_create(nombre='Ecuador')
    
    # Lista de todas las provincias del Ecuador
    provincias_ecuador = [
        "Azuay",
        "Bolívar", 
        "Cañar",
        "Carchi",
        "Chimborazo",
        "Cotopaxi",
        "El Oro",
        "Esmeraldas",
        "Galápagos",
        "Guayas",
        "Imbabura",
        "Loja",
        "Los Ríos",
        "Manabí",
        "Morona Santiago",
        "Napo",
        "Orellana",
        "Pastaza",
        "Pichincha",
        "Santa Elena",
        "Santo Domingo de los Tsáchilas",
        "Sucumbíos",
        "Tungurahua",
        "Zamora Chinchipe"
    ]
    
    # Crear cada provincia
    for nombre_provincia in provincias_ecuador:
        Provincia.objects.get_or_create(
            nombre=nombre_provincia,
            pais=ecuador
        )

def reverse_add_ecuador_provinces(apps, schema_editor):
    # Función para revertir la migración
    Pais = apps.get_model('store', 'Pais')
    Provincia = apps.get_model('store', 'Provincia')
    
    ecuador = Pais.objects.filter(nombre='Ecuador').first()
    if ecuador:
        Provincia.objects.filter(pais=ecuador).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_update_ecuadorian_descriptions'),
    ]

    operations = [
        migrations.RunPython(add_ecuador_provinces, reverse_add_ecuador_provinces),
    ] 