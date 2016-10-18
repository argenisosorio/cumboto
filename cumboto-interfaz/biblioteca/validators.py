from django.core.exceptions import ValidationError
 
def valid_extension(value):
    if (not value.name.endswith('.zip') and
        not value.name.endswith('.tar.gz')):
       
 
        raise ValidationError("Archivos permitidos: .zip, .tar.gz")
