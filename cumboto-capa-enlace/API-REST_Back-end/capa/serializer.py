# -*- coding: utf-8 -*-
from .models import appModel
from .models import Archivo

from rest_framework import serializers


class appSerializer(serializers.ModelSerializer):
    """
    Clase que permite serializar los datos de persona
    Autor: Luis Guillermo Echenque (lechenique@gmail.com)
    fecha: 22-05-2017
    """
    doc = serializers.FileField(max_length=None,use_url=True)

    class Meta:
        model = Archivo
        fields = ('id_app', 'codigo_app', 'version', 'archivo_nombre','descomprimido','fecha_creado','doc')
