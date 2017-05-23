# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _


class appModel(models.Model):

    codigo_app = models.CharField(max_length=12, help_text=_("Codigo de la aplicacion"),)

class Archivo(models.Model):
    codigo_app = models.CharField(max_length=12,  help_text=_("Codigo de la aplicacion"),)
    archivo_nombre = models.CharField(max_length=20)
    fecha_creado = models.DateTimeField(auto_now=True)
    descomprimido = models.BooleanField(default=False)
    doc = models.FileField(upload_to='Doc/',default='Doc/None/No-doc.zip')
    id_app = models.CharField(max_length=25, primary_key=True)
    version = models.CharField(max_length=25,)

    def __str__(self):
        return "%s" % self.archivo_nombre
