# -*- coding: utf-8 -*-
from .models import appModel

from rest_framework import serializers


class appSerializer(serializers.ModelSerializer):
    """
    Clase que permite serializar los datos de persona
    """

    class Meta:
        model = appModel
        fields = ('codigo_app')
