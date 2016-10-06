# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import servicioModel
from django.forms.models import ModelForm
import ocumare
#from .views import CONSULT_REST
from ocumare.lutheria import tsco


class servicioForm(ModelForm):

    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    lst = octs.obt_serv_md()
    opciones = ()
    for x in lst:
        opciones += (x['codigo'], x['n']),
    servicio = forms.ChoiceField(
        choices=opciones,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
        })
    )

    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    lst = octs.obt_serv_md()
    ranuras = ()
    for i in lst:
        if i['na'] == 2:
            ranuras = ('', _("Seleccione...")),\
           ('1', _("Ranura_1")),\
           ('2', _("Ranura_2")),\

    ranura = forms.ChoiceField(
        choices=ranuras,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',

        })
    )

    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    app = octs.obt_apps_biblio()
    apps = ()
    for a in app:
        apps += (a['codigo'], a['nombre']),

    codigo_app = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'false',
            'disabled': 'disabled',

        }), choices=apps, required=False,
    )

    List_Mod = ('', _("Seleccione...")),\
           ('1', _("Automatico")),\
           ('2', _("Menu")),\

    modalidad = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'false',
            'disabled': 'disabled',
        }),choices=List_Mod, required=False,
    )

    detener = forms.ChoiceField(
        label=_("Detener Servicio"),
        choices=((True,''), (False,'')),
        widget=forms.CheckboxInput(attrs={
                'class': 'correr_detener', 'data-rule-required': 'true', 'data-toggle': 'tooltip',
                'title': _("Detener un Servicio"),
                'onchange': "habilitar($(this).is(':checked'), codigo_app.id), habilitar($(this).is(':checked'), modalidad.id)",
            }
        )
    )

    class Meta:
        model = servicioModel
        fields = ('codigo_app',)

class SelectForm(forms.Form):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    lst = octs.obt_serv_md()
    opciones = ()
    for x in lst:
        opciones += (x['codigo'],x['n']),
    select_serv = forms.ChoiceField(
        choices=opciones,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
        })
    )
