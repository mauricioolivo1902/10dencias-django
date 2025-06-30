from django import forms
from .models import DatosFacturacion, Provincia, Ciudad
from .validators import ValidatorFactory

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = DatosFacturacion
        fields = [
            'nombre', 'apellido', 'numero_identificacion', 
            'pais', 'provincia', 'ciudad', 'direccion_linea_1'
        ]
        
    def clean_numero_identificacion(self):
            """
            Método de validación refactorizado. Ahora delega la lógica a un validador externo.
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # --- Personalización de placeholders (sin cambios) ---
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Tu nombre'})
        self.fields['apellido'].widget.attrs.update({'placeholder': 'Tu apellido'})
        self.fields['numero_identificacion'].widget.attrs.update({'placeholder': 'Ej: 1712345678'})
        self.fields['direccion_linea_1'].widget.attrs.update({'placeholder': 'Calle Principal y Secundaria'})
        
        # --- LÓGICA CORREGIDA PARA DESPLEGABLES DINÁMICOS ---

        # Por defecto, los querysets están vacíos. Esto es para la carga inicial (GET).
        self.fields['provincia'].queryset = Provincia.objects.none()
        self.fields['ciudad'].queryset = Ciudad.objects.none()

        # self.data contiene los datos de una petición POST.
        # Si el formulario se está cargando con datos de un envío...
        if self.data:
            try:
                # Obtenemos el ID del país que se envió.
                pais_id = int(self.data.get('pais'))
                # Re-poblamos el queryset de provincias para que la validación funcione.
                self.fields['provincia'].queryset = Provincia.objects.filter(pais_id=pais_id).order_by('nombre')
            except (ValueError, TypeError):
                # Si hay un error (ej. no se envió un país), ignoramos para que la validación normal falle.
                pass
            
            try:
                # Hacemos lo mismo para la ciudad.
                provincia_id = int(self.data.get('provincia'))
                self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        # Esta lógica también funcionaría si inicializas el formulario con una 'instance' existente.
        elif self.instance.pk:
            if self.instance.pais:
                self.fields['provincia'].queryset = self.instance.pais.provincia_set.order_by('nombre')
            if self.instance.provincia:
                self.fields['ciudad'].queryset = self.instance.provincia.ciudad_set.order_by('nombre')


    def clean_numero_identificacion(self):
        # --- Lógica de validación (sin cambios) ---
        numero = self.cleaned_data.get('numero_identificacion')
        if not numero:
            raise forms.ValidationError("Este campo es obligatorio.")
        if not numero.isdigit():
            raise forms.ValidationError("El número de identificación solo debe contener dígitos.")
        if len(numero) != 10:
            raise forms.ValidationError("El número de identificación debe tener exactamente 10 dígitos.")
        return numero