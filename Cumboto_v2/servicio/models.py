from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class servicioModel(models.Model):

    codigo_app = models.CharField(
        max_length=12, help_text=_("Codigo de la aplicacion"),
    )

