# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import appModel
from django.forms.models import ModelForm
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput,
    Select)

List_App = ('', _("Seleccione...")),\
           ('0000000A0020', _("0000000A0020")),\
           ('0000000A0030', _("0000000A0030")),\
           ('0000000A0040', _("0000000A0040")),\
           ('0000000A0064', _("0000000A0064")),

List_Serv = ('', _("Seleccione...")),\
           ('0', _("0")),\
           ('1', _("1")),\
           ('2', _("2")),\
           ('3', _("3")),\
           ('4', _("4")),

List_ran = ('', _("Seleccione...")),\
           ('0', _("0")),\
           ('1', _("1")),\

List_Mod = ('', _("Seleccione...")),\
           ('1', _("1")),\
           ('2', _("2")),\




class appForm(ModelForm):
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
        choices=List_App,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
        })
    )
    modalidad = forms.ChoiceField(
        choices=List_Mod,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'true',
        })
    )

    class Meta:
        model = appModel
        fields = ('codigo_app',)