from django import forms
from .models import DatosFacturacion, Provincia, Ciudad, Pais, Cupon
from .validators import ValidatorFactory

# Patrón: Form Object
# Este formulario encapsula la validación y procesamiento de datos del usuario.
class CheckoutForm(forms.Form):
    nombre = forms.CharField(max_length=200)
    apellido = forms.CharField(max_length=200)
    numero_identificacion = forms.CharField(max_length=20)
    pais = forms.ModelChoiceField(queryset=Pais.objects.all())
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.none())
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.none())
    direccion_linea_1 = forms.CharField(max_length=200)
    cupon = forms.CharField(max_length=50, required=False, label="Cupón de descuento")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].queryset = Pais.objects.all()
        self.fields['provincia'].queryset = Provincia.objects.none()
        self.fields['ciudad'].queryset = Ciudad.objects.none()
        
        # --- Personalización de placeholders ---
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Tu nombre'})
        self.fields['apellido'].widget.attrs.update({'placeholder': 'Tu apellido'})
        self.fields['numero_identificacion'].widget.attrs.update({'placeholder': 'Ej: 1712345678'})
        self.fields['direccion_linea_1'].widget.attrs.update({'placeholder': 'Calle Principal y Secundaria'})
        
        # --- Configurar Ecuador como país por defecto ---
        try:
            ecuador = Pais.objects.get(nombre='Ecuador')
            self.fields['pais'].initial = ecuador.id
            # Cargar provincias de Ecuador por defecto
            self.fields['provincia'].queryset = Provincia.objects.filter(pais=ecuador).order_by('nombre')
        except Pais.DoesNotExist:
            # Si Ecuador no existe, mantener querysets vacíos
            self.fields['provincia'].queryset = Provincia.objects.none()
            self.fields['ciudad'].queryset = Ciudad.objects.none()

        # Si hay datos en el formulario, actualiza los queryset de provincia y ciudad
        if 'pais' in self.data:
            try:
                pais_id = int(self.data.get('pais'))
                self.fields['provincia'].queryset = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('pais'):
            pais_id = self.initial.get('pais').id if hasattr(self.initial.get('pais'), 'id') else self.initial.get('pais')
            self.fields['provincia'].queryset = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')

        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.initial.get('provincia'):
            provincia_id = self.initial.get('provincia').id if hasattr(self.initial.get('provincia'), 'id') else self.initial.get('provincia')
            self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')

    def clean_numero_identificacion(self):
        """
        Patrón: Strategy + Factory
        Usa ValidatorFactory (Factory) para obtener la estrategia de validación adecuada (Strategy) según el país.
        Principios SOLID: OCP (puedes agregar validadores sin modificar el formulario), DIP (el formulario depende de una abstracción).
        """
        # Obtenemos los datos que necesitamos: el número y el país.
        numero = self.cleaned_data.get('numero_identificacion')
        pais = self.cleaned_data.get('pais')

        if not numero or not pais:
            # Si falta alguno de los datos clave, la validación de campo obligatorio actuará.
            return numero

        # ¡Magia! Le pedimos a la fábrica el validador correcto.
        validator = ValidatorFactory.get_validator(pais.nombre)

        # Si existe un validador para ese país, lo usamos.
        if validator:
            # La forma no sabe qué validador es, solo que puede llamar a .validate()
            # ¡Esto es Inversión de Dependencias!
            return validator.validate(numero)
        
        # Si no hay validador específico, simplemente devolvemos el número sin validación extra.
        return numero