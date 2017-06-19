# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    """
    Modelos de los campos extra del perfil del usuario
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 06-06-2017
    """
    # Establece la relación entre el usuario de Django y el perfil
    #user = models.OneToOneField(User,unique=True)
    #user = models.OneToOneField(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Establece el Cargo que ocupa el usuario
    cargo = models.CharField(max_length=50)

    # Establece el nivel de Formación Académica del usuario
    #formacion = models.CharField(max_length=50)

    def __unicode__(self):
        return self.cargo
