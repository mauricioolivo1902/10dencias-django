# Archivo de migración
# Permite corregir los nombres de las provincias en la base de datos.

from django.db import migrations

def fix_province_names(apps, schema_editor):
    # Obtenemos los modelos
    Pais = apps.get_model('store', 'Pais')
    Provincia = apps.get_model('store', 'Provincia')
    
    # Obtenemos Ecuador
    ecuador = Pais.objects.get(nombre='Ecuador')
    
    # Cambiar "Santo Domingo de los Tsáchilas" por "Santo Domingo"
    try:
        provincia_santo_domingo = Provincia.objects.get(
            nombre="Santo Domingo de los Tsáchilas",
            pais=ecuador
        )
        provincia_santo_domingo.nombre = "Santo Domingo"
        provincia_santo_domingo.save()
    except Provincia.DoesNotExist:
        pass

def reverse_fix_province_names(apps, schema_editor):
    # Función para revertir la migración
    Pais = apps.get_model('store', 'Pais')
    Provincia = apps.get_model('store', 'Provincia')
    
    ecuador = Pais.objects.get(nombre='Ecuador')
    
    # Revertir "Santo Domingo" a "Santo Domingo de los Tsáchilas"
    try:
        provincia_santo_domingo = Provincia.objects.get(
            nombre="Santo Domingo",
            pais=ecuador
        )
        provincia_santo_domingo.nombre = "Santo Domingo de los Tsáchilas"
        provincia_santo_domingo.save()
    except Provincia.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_add_ecuador_cities'),
    ]

    operations = [
        migrations.RunPython(fix_province_names, reverse_fix_province_names),
    ] 