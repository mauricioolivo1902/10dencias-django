from django.core.exceptions import ValidationError

class IDValidator:
    """
    Clase base que actúa como nuestra "Interfaz" para los validadores.
    El formulario dependerá de esta abstracción, no de las clases concretas.
    """
    def validate(self, id_number):
        raise NotImplementedError("El método 'validate' debe ser implementado por las subclases.")

class EcuadorianIDValidator(IDValidator):
    """ Validador específico para la cédula ecuatoriana. """
    def validate(self, id_number):
        if not id_number.isdigit():
            raise ValidationError("El número de identificación solo debe contener dígitos.")
        if len(id_number) != 10:
            raise ValidationError("La cédula ecuatoriana debe tener exactamente 10 dígitos.")
        # Aquí podría ir el algoritmo completo de validación de la cédula ecuatoriana.
        return id_number

class ColombianIDValidator(IDValidator):
    """ Validador de ejemplo para la cédula colombiana. """
    def validate(self, id_number):
        if not id_number.isdigit():
            raise ValidationError("El número de identificación solo debe contener dígitos.")
        if not 7 <= len(id_number) <= 11:
            raise ValidationError("La cédula colombiana debe tener entre 7 y 11 dígitos.")
        return id_number

class ValidatorFactory:
    """
    Esta es nuestra Fábrica. Su única responsabilidad es crear y devolver
    el objeto validador correcto según el país.
    """
    @staticmethod
    def get_validator(country_name):
        if country_name.lower() == 'ecuador':
            return EcuadorianIDValidator()
        if country_name.lower() == 'colombia':
            return ColombianIDValidator()
        # Si el país no tiene un validador específico, no devolvemos nada.
        return None