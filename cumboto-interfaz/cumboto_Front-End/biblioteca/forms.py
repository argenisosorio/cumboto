# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from biblioteca.models import registrar_app
from django.utils.translation import ugettext_lazy as _


class registrar_form(ModelForm):
    """!
    Clase del formulario para registrar aplicaciones en la biblioteca
    Autor: Hugo Ramírez (hramirez@cenditel.gob.ve)
    Fecha: 2016
    """
    cargar_app = forms.FileField(label=("Cargar Aplicación"),widget=forms.FileInput(attrs={
        'class': 'filestyle',
        'type': 'file',
        'data-placeholder' : 'Archivos permitidos: .zip ',
        'data-buttonName' : 'btn-default',
        'data-toggle': 'tooltip',
        'data-buttonText': 'Buscar archivo',
        'data-classInput' : 'input-small',
        'data-size':'sm',
        'required': 'true',
        'title': _("Seleccione el zip que contenga la Aplicacion a cargar"),
    }))

    class Meta:
        model = registrar_app
        fields=['cargar_app']