# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _


class appModel(models.Model):

    codigo_app = models.CharField(
        max_length=12, help_text=_("Codigo de la aplicacion"),
        #validators=[
            #validators.RegexValidator(
              #  r'^[\d]+$',
               # _("Codigo de aplicacion inválido. Solo se permiten numeros")
            #),
        #]
    )
