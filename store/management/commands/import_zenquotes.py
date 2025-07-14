from django.core.management.base import BaseCommand
from store.models import FraseMotivacional
import requests

class Command(BaseCommand):
    help = 'Importa frases desde la API pública de ZenQuotes y las guarda en la base de datos.'

    def handle(self, *args, **kwargs):
        url = 'https://zenquotes.io/api/quotes'
        self.stdout.write('Obteniendo frases desde ZenQuotes...')
        try:
            response = requests.get(url)
            response.raise_for_status()
            frases = response.json()
            count = 0
            for frase in frases:
                texto = f"{frase.get('q')} — {frase.get('a')}"
                # Evita duplicados
                if not FraseMotivacional.objects.filter(texto=texto).exists():
                    FraseMotivacional.objects.create(texto=texto)
                    count += 1
            self.stdout.write(self.style.SUCCESS(f'Se importaron {count} frases nuevas.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al importar frases: {e}')) 