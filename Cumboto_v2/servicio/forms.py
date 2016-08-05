# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import servicioModel
from django.forms.models import ModelForm


List_App = ('', _("Seleccione...")),\
           ('0000000A0020', _("0000000A0020")),\
           ('0000000A0030', _("0000000A0030")),\
           ('0000000A0040', _("0000000A0040")),\
           ('0000000A0064', _("0000000A0064")),

List_Serv = ('', _("Seleccione...")),\
           ('0', _("Tves")),\
           ('1', _("Vive")),\
           ('2', _("2")),\
           ('3', _("3")),\
           ('4', _("4")),

List_ran = ('', _("Seleccione...")),\
           ('0', _("0")),\
           ('1', _("1")),\


List_Mod = ('', _("Seleccione...")),\
           ('1', _("1")),\
           ('2', _("2")),\

class servicioForm(ModelForm):

    servicio = forms.ChoiceField(
        choices=List_Serv,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',


        })
    )
    ranura = forms.ChoiceField(
        choices=List_ran,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',

        })
    )
    codigo_app = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'false',
            'disabled': 'disabled',

        }), choices=List_App, required=False,
    )
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


