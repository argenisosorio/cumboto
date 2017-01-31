from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class servicioModel(models.Model):

    servicio = models.CharField(
        max_length=12, help_text=_("Servicios disponible"),primary_key=True
    )

    ranura_int = models.IntegerField(
        help_text=_("Numero de ranura"),
    )

    ranura_str = models.CharField(
        max_length=12, help_text=_("Ranura str"),
    )

    codigo_int = models.CharField(
        max_length=12, help_text=_("Codigo de la aplicacion"),
    )

    nombre = models.CharField(
    max_length=12, help_text=_("Nombre de la aplicacion"),
    )

    modalidad_int = models.CharField(
        max_length=12, help_text=_("Modalidad en la que se encuentra la aplicacion"),
    )

    modalidad_str = models.CharField(
        max_length=12, help_text=_("Modalidad en la que se encuentra la aplicacion"),
    )

class DataModelo(models.Model):

    ranura = models.IntegerField(verbose_name="full name")
    codigo_app = models.CharField(verbose_name="full name", max_length=100)
    modalidad = models.CharField(verbose_name="full name", max_length=100)
