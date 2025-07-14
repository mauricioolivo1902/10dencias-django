# Archivo de migración
# Permite agregar las ciudades principales de Ecuador a la base de datos.

from django.db import migrations

def add_ecuador_cities(apps, schema_editor):
    # Obtenemos los modelos
    Pais = apps.get_model('store', 'Pais')
    Provincia = apps.get_model('store', 'Provincia')
    Ciudad = apps.get_model('store', 'Ciudad')
    
    # Obtenemos Ecuador
    ecuador = Pais.objects.get(nombre='Ecuador')
    
    # Diccionario con provincias y sus principales ciudades
    ciudades_por_provincia = {
        "Azuay": ["Cuenca", "Gualaceo", "Paute", "Sigsig", "Chordeleg"],
        "Bolívar": ["Guaranda", "San Miguel", "Caluma", "Chillanes", "Echeandía"],
        "Cañar": ["Azogues", "Biblián", "Cañar", "La Troncal", "El Tambo"],
        "Carchi": ["Tulcán", "Mira", "Espejo", "Montúfar", "San Pedro de Huaca"],
        "Chimborazo": ["Riobamba", "Guano", "Colta", "Penipe", "Guamote"],
        "Cotopaxi": ["Latacunga", "La Maná", "Pangua", "Pujilí", "Salcedo"],
        "El Oro": ["Machala", "El Guabo", "Pasaje", "Santa Rosa", "Huaquillas"],
        "Esmeraldas": ["Esmeraldas", "Atacames", "Muisne", "Quinindé", "San Lorenzo"],
        "Galápagos": ["Puerto Baquerizo Moreno", "Puerto Ayora", "Puerto Villamil"],
        "Guayas": ["Guayaquil", "Daule", "Durán", "El Triunfo", "Milagro"],
        "Imbabura": ["Ibarra", "Otavalo", "Cotacachi", "Antonio Ante", "Pimampiro"],
        "Loja": ["Loja", "Catamayo", "Paltas", "Calvas", "Puyango"],
        "Los Ríos": ["Babahoyo", "Quevedo", "Ventanas", "Vinces", "Palenque"],
        "Manabí": ["Portoviejo", "Manta", "Montecristi", "Jipijapa", "Chone"],
        "Morona Santiago": ["Macas", "Gualaquiza", "Limón Indanza", "Palora", "Santiago"],
        "Napo": ["Tena", "Archidona", "El Chaco", "Quijos", "Carlos Julio Arosemena Tola"],
        "Orellana": ["Francisco de Orellana", "Aguarico", "La Joya de los Sachas", "Loreto"],
        "Pastaza": ["Puyo", "Mera", "Santa Clara", "Arajuno"],
        "Pichincha": ["Quito", "Cayambe", "Mejía", "Pedro Moncayo", "Rumiñahui"],
        "Santa Elena": ["Santa Elena", "La Libertad", "Salinas"],
        "Santo Domingo de los Tsáchilas": ["Santo Domingo", "La Concordia"],
        "Sucumbíos": ["Nueva Loja", "Gonzalo Pizarro", "Putumayo", "Shushufindi", "Sucumbíos"],
        "Tungurahua": ["Ambato", "Baños de Agua Santa", "Cevallos", "Mocha", "Patate"],
        "Zamora Chinchipe": ["Zamora", "Chinchipe", "Nangaritza", "Yacuambi", "El Pangui"]
    }
    
    # Crear ciudades para cada provincia
    for nombre_provincia, ciudades in ciudades_por_provincia.items():
        try:
            provincia = Provincia.objects.get(nombre=nombre_provincia, pais=ecuador)
            for nombre_ciudad in ciudades:
                Ciudad.objects.get_or_create(
                    nombre=nombre_ciudad,
                    provincia=provincia
                )
        except Provincia.DoesNotExist:
            print(f"Provincia '{nombre_provincia}' no encontrada")

def reverse_add_ecuador_cities(apps, schema_editor):
    # Función para revertir la migración
    Ciudad = apps.get_model('store', 'Ciudad')
    Ciudad.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_add_ecuador_provinces'),
    ]

    operations = [
        migrations.RunPython(add_ecuador_cities, reverse_add_ecuador_cities),
    ] 