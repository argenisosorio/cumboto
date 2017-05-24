#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.forms import (
    ModelForm, TextInput, EmailInput, CharField, EmailField, PasswordInput,
    Select
)


class LoginForm(AuthenticationForm):
    """
    Clase del formulario de inicio de sesíon de los usuarios
    Autor: Hugo Ramírez (hramirez@cenditel.gob.ve)
    Fecha: 2016
    """
    username = forms.CharField(
        label=("username"),
        widget=forms.TextInput(attrs={
            'class': 'form-control col-md-5 col-xs-16',
            'type': 'text',
            'id': 'id_username',
            'name': 'username',
            'placeholder': 'Usuario',
            'autofocus': 'autofocus',
            'title':'Ingrese su nombre de usuario',
            'required': 'true'
        })
    )

    password = forms.CharField(
        label=("Password"), 
        max_length=30, 
        widget=PasswordInput(attrs={
            'class': 'item form-group',
            'placeholder': _("contraseña de acceso"),
            'data-toggle': 'tooltip',
            'title': _("Indique la contraseña de acceso al sistema"), 'size': '28',
        })
    )

    def Valid_usuaio(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError(_("El usuario indicado no existe"))

        return username
            
    def Valid_pass(self):
        password = self.cleaned_data['password']
        if not User.objects.filter(password=password):
            raise forms.ValidationError(_("La contraseña indicada es incorrecta"))

        return password

class UserForm(UserCreationForm):
    """
    Clase del formulario que registra los usuarios
    Autor: Hugo Ramírez (hramirez@cenditel.gob.ve)
    Fecha: 2016
    """
    first_name = forms.CharField(
        label=("Nombres"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'required': 'true',
            'title':'Ingrese su nombre completo',
            'id': 'first_name',
            'data-toggle': 'tooltip',
            'placeholder': 'Nombres',
        })
    )
    
    last_name = forms.CharField(
        label=("Apellidos"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'required': 'true',
            'title':'Ingrese sus apellidos completo',
            'id': 'last_name',
            'data-toggle': 'tooltip',
            'placeholder': 'Apellidos',
        })
    )

    email = forms.CharField(
        label=("Email"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'email',
            'placeholder': 'Dirección de correo',
            'required': 'true',
            'data-toggle': 'tooltip',
            'title':'Ingrese su email',
            'id': 'email',
        })
    )

    username = forms.CharField(max_length=30, label=("Usuario"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'true',
            'placeholder': 'Nombre de usuario',
            'title':'Ingrese el nombre de usuario',
            'data-toggle': 'tooltip',
            'id': 'username',
        })
    )

    password1 = forms.CharField(
        label=("Contraseña"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'required': 'true',
            'placeholder': 'Contraseña',
            'title':'Ingrese la contraseña de su preferencia',
            'data-toggle': 'tooltip',
            'id': 'password1',
        })
    )

    password2 = forms.CharField(
        label=("Contraseña (confirmación)"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'required': 'true',
            'placeholder': 'Vuelva a ingresar la contraseña elegida',
            'data-toggle': 'tooltip',
            'id': 'password2',
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'email', 'username', 'password1', 'password2')

    def clean_username(self):
        """
        Método que verifica si el campo username es menor a 3 caractéres.
        Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
        Fecha: 19-05-2017
        """
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError("El username debe tener mas de 3 caractéres")
        return username

    def clean_email(self):
        """
        Método que valida si el email a registrar ya existe
        Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
        Fecha: 19-05-2017
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email


class EditarEmailForm(forms.Form):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super().__init__(*args, **kwargs)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # Comprobar si ha cambiado el email
        actual_email = self.request.user.email
        username = self.request.user.username
        if email != actual_email:
            # Si lo ha cambiado, comprobar que no exista en la db.
            # Exluye el usuario actual.
            existe = User.objects.filter(email=email).exclude(username=username)
            if existe:
                raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

class EditarContrasenaForm(forms.Form):
    actual_password = forms.CharField(
        label='Contraseña actual',
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Nueva contraseña',
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir contraseña',
        min_length=3,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


class EditProfileForm(forms.ModelForm):
    """
    Clase del formulario que permite editar el perfil del usuario autenticado.
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 03-04-2017
    """

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Dirección de correo electrónico',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class':'form-control input-md',
            }),
            'first_name': forms.TextInput(attrs={
                'class':'form-control input-md',
            }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control input-md',
            }),
            'email': forms.TextInput(attrs={
                'class':'form-control input-md',
            }),
        }