# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    """
    Modelo para guardar el Perfil de usuario
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 06-06-2017
    """

    # Establece la relación entre el usuario de Django y el perfil.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Establece el Cargo que ocupa el usuario.
    cargo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.cargo


class Bitacora(models.Model):
    """
    Modelo para guardar la bitácora de acciones del usuario
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 06-07-2017
    """
    # Establece el usuario que realizó la acción.
    usuario=models.CharField(max_length=200)

    # Breve descripción de la acción realizada.
    descripcion = models.CharField(max_length=200)

    # Establece el tipo de acción realizada (acceso, etc)
    tipo = models.CharField(max_length=50)

    # Establece la fecha y hora en que se realizó la acción.
    fecha_hora = models.DateField()

    def __unicode__(self):
        return self.usuario
