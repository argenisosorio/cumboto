# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import servicioModel
from django.forms.models import ModelForm
import requests
import json
from django.conf import settings


class servicioForm(ModelForm):
    api = requests.get(settings.URL_API_REST+'api_rest/listar?format=json')
    servicios = api.content
    decode_data = json.loads(servicios)
    opciones = ()
    for x in range(len(decode_data)):
        j = decode_data[x]
        opciones += (j['codigo'], j['n']),

    # Esto solo tiene que estar en interfaz y esperar que la capa responda
    servicio = forms.ChoiceField(
        choices=opciones,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'id': 'servicio',
            'title': _("Selecione el servicio que desea"),
        })
    )

    # No siempre las ranuras son uno y dos mejorar el metodo #
    # FALTA FILTRAR POR EL SERVICIO SELECCIONADO PARA QUE APAREZCA LAS RANURAS ASIGNADA A ESE SERVICIO, SI
    # COMO ESTA LISTAS LAS RANURAS DE TODOS LOS SERVICIOS, QUE TRAE EL DECODE_DATA)
    ranuras = ()
    for i in decode_data:
        print decode_data
        r = i['na']
        for j in range(r):
               ranuras +=('%s' % j, _('Ranura %s' % j )),
#               ranuras += ('', _("Seleccione...")),\
#               ('%s' % j, _('Ranura %s' % j ))
#        if i['na'] == 2:
#            ranuras = ('', _("Seleccione...")),\
#           ('0', _("Ranura 0")),\
#           ('1', _("Ranura 1")),\
#
#        if i['na'] == 1:
#            ranuras = ('', _("Seleccione...")),\
#           ('0', _("Ranura 0")),\

    ranura = forms.ChoiceField(
        choices=ranuras,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'id': 'ranura',
            'title': _("Selecione la ranura que desea"),

        })
    )

    ## Consulta a la biblioteca del servidor
    listar_aplicaciones = requests.get(settings.URL_API_REST+'api_rest/listar-aplicaciones?format=json')
    lista = listar_aplicaciones.content
    loads_data = json.loads(lista)

    apps = ()
    for x in range(len(loads_data)):
        j = loads_data[x]
        apps += (j['codigo'], j['nombre']),

    codigo_app = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'title': _("Selecione la aplicacion que desea"),
            'id': 'codigo_app',

        }), choices=apps, required=False,
    )

    List_Mod = ('', _("Seleccione...")),\
           ('1', _("Automatico")),\
           ('2', _("Menu")),\

    modalidad = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'title': _("Selecione la modalidad que desea"),
            'id': 'modalidad',
        }),choices=List_Mod, required=False,
    )

    detener = forms.ChoiceField(
        label=_("Detener Servicio"),
        choices=((True,''), (False,'')),
        widget=forms.CheckboxInput(attrs={
                'class': 'js-switch', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Detener un Servicio"),
                'onchange': "habilitar($(this).is(':checked'), codigo_app.id), habilitar($(this).is(':checked'), modalidad.id)",
                'id': 'detener',
            }
        )
    )

    class Meta:
        model = servicioModel
        fields = ('codigo_app',)

class SelectForm(forms.Form):

    api = requests.get(settings.URL_API_REST+'api_rest/listar?format=json')
    servicios = api.content
    decode_data = json.loads(servicios)
    opciones = ()
    for x in range(len(decode_data)):
        j = decode_data[x]
        opciones += (j['codigo'], j['n']),
    select_serv = forms.ChoiceField(
        choices=opciones,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
            'id': 'servicio',
            'title': _("Selecione el servicio que desea"),
        })
    )
