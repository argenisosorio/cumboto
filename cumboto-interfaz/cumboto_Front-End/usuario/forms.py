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
    username = forms.CharField(
        label=("username"),
        widget=forms.TextInput(attrs={'class': 'form-control col-md-5 col-xs-16',
                                      'type': 'text',
                                      'id': 'id_username',
                                      'name': 'username',
                                      'placeholder': 'Usuario',
                                      'autofocus': 'autofocus',
                                      'title':'Ingrese su nombre de usuario',
                                      'required': 'true'})) 
    password = forms.CharField(
        label=("Password"), 
        max_length=30, 
        widget=PasswordInput(attrs={
            'class': 'item form-group', 'placeholder': _("contraseña de acceso"), 'data-toggle': 'tooltip',
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

    first_name = forms.CharField(
        label=("Nombres"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'text',
                                      'required': 'true',
                                      'title':'Ingrese su nombre completo',
                                      'id': 'first_name',
                                      'data-toggle': 'tooltip',
                                      'placeholder': 'Nombres'
        }),
    )
    
    last_name = forms.CharField(
        label=("Apellidos"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'text',
                                      'required': 'true',
                                      'title':'Ingrese sus apellidos completo',
                                      'id': 'last_name',
                                      'data-toggle': 'tooltip',
                                      'placeholder': 'Apellidos'
        }),
    )

    email = forms.CharField(
        label=("Email"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'email',
                                      'placeholder': 'Dirección de correo',
                                      'required': 'true',
                                      'data-toggle': 'tooltip',
                                      'title':'Ingrese su email',
                                      'id': 'email',
        })
    )

    
    username = forms.RegexField(
    label=("Usuario"), max_length=30, regex=r"^[\w.@+-]+$",
    error_messages={
        'invalid':("Este campo debe contener solo letras numeros y los siguientes caracteres "
                     "@/./+/-/_")},
    widget=forms.TextInput(attrs={'class': 'form-control',
                            'required': 'true',
                            'placeholder': 'Nombre de usuario',
                            'title':'Ingrese el nombre de usuario',
                            'data-toggle': 'tooltip',
                            'id': 'username',
        })
    )

    password1 = forms.CharField(
        label=("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                      'required': 'true',
                                      'placeholder': 'Contraseña',
                                      'title':'Ingrese la contraseña de su preferencia',
                                      'data-toggle': 'tooltip',
                                      'id': 'password1',
                                      
        })
    )
    password2 = forms.CharField(
        label=("Contraseña (confirmación)"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'password',
                                          'required': 'true',
                                          'placeholder': 'Vuelva a ingresar la contraseña elegida',
                                          'data-toggle': 'tooltip',
                                          'id': 'password2'
        }),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'email', 'username', 'password1', 'password2')

    def Valid_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError(_("El usuario indicado ya existe"))

        return username

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2  
    
    def save(self, commit = True):      
        user = User.objects.create_user(self.cleaned_data['username'],
                                     self.cleaned_data['email'],
                                     self.cleaned_data['password1'])
        user.is_active = False
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        user.save()
            
        return user


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
    #username = forms.CharField(label='Nombre de usuario')
    #first_name = forms.CharField(label='Primer nombre')
    #last_name = forms.CharField(label='Apellido')
    #email = forms.EmailField(label='Email')

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
                #'style': 'min-width: 0; width: 50%; display: inline;',
            }),
            'first_name': forms.TextInput(attrs={
                'class':'form-control input-md',
                #'style': 'min-width: 0; width: 50%; display: inline;',
            }),
            'last_name': forms.TextInput(attrs={
                'class':'form-control input-md',
                #'style': 'min-width: 0; width: 50%; display: inline;',
            }),
            'email': forms.TextInput(attrs={
                'class':'form-control input-md',
                #'style': 'min-width: 0; width: 50%;',
            }),
        }