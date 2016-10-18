# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.hashers import make_password
from .models import Profile



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=("username"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'text',
                                      'placeholder': 'Usuario',
                                      'required': 'true'})) 
    password = forms.CharField(
        label=("Password"), 
        max_length=30, 
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'name': 'password',
                                      'required': 'true'}))


@python_2_unicode_compatible
class UserForm(UserCreationForm):
    first_name = forms.CharField(
        label=("Nombres"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'text',
                                      'required': 'true',
        }),
    )
    
    last_name = forms.CharField(
        label=("Apellidos"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'text',
                                      'required': 'true',
        }),
    )

    email = forms.CharField(
        label=("Email"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'email',
                                      'placeholder': 'Dirección de correo',
                                      'required': 'true'
        })
    )
    
    username = forms.RegexField(
    label=("Usuario"), max_length=30, regex=r"^[\w.@+-]+$",
    #help_text=("Requerido. 30 caracteres. Letters, digits and "
                #"@/./+/-/_ only."),
    error_messages={
        'invalid':("Este campo debe contener solo letras numeros y los siguientes caracteres "
                     "@/./+/-/_")},
    widget=forms.TextInput(attrs={'class': 'form-control',
                            'required': 'true',
                            'placeholder': 'Nombre de usuario',
        })
    )
    
    password1 = forms.CharField(
        label=("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                      'required': 'true',
        })
    )
    password2 = forms.CharField(
        label=("Contraseña (confirmación)"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'password',
                                          'required': 'true',
                                          'placeholder': 'Vuelva a ingresar la contraseña'
        }),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name',  'email', 'username', 'password1', 'password2')

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

class PerfilForm(UserForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2',
        ]


    def __init__(self, *args, **kwargs):

        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['verificar_contrasenha'].required = False
        if self.data.__contains__('password') and self.data['password'] != '':
            self.fields['password'].required = True
            self.fields['password2'].required = True
        self.fields['password'].help_text = 'passwordMeterId'

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la db.')
        return email

    def clean_password(self):
        if self.cleaned_data['password'] != '':
            password_meter = self.data['passwordMeterId']
            if int(password_meter) < FORTALEZA_CONTRASENHA:
                raise forms.ValidationError(_("La contraseña es débil"))

        return self.cleaned_data['password']




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
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Nueva contraseña',
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir contraseña',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cedula', 'telefono', 'cargo', 'canal')