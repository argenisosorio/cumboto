from django.db import models
from django.core.files.base import File
from biblioteca.validators import valid_extension
import os


def generate_path(instance, filename):
 
    folder = os.path.join("aplicacion", filename)
    return folder
    #folder = "aplicacion" + str(instance.user) 
    #return os.path.join("aplicacion", folder, filename)

class registrar_app(models.Model):
    cargar_app = models.FileField(
        blank=True, null=True, upload_to=generate_path,
                validators=[valid_extension])
    
    def __str__(self):             
        return self.cargar_app

