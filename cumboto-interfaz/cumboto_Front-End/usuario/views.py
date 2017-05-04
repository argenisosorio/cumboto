# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context,  RequestContext
from django.contrib.auth.models import User
from .forms import UserForm, LoginForm, EditarEmailForm, EditarContrasenaForm, EditProfileForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView, FormView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import urlresolvers
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, CreateView, ListView
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template import loader, Context
from django.views import generic
from django.views.generic import DeleteView
import logging
logger = logging.getLogger("usuario")


def acceso(request):
    """
    Función que gestiona la autenticación de los usuarios, maneja estatus de no logeado, inactivo en espera de activación y sin usuario creado.
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 13-02-2017
    """
    if not request.user.is_anonymous():
        return render_to_response('base.login.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return render_to_response('home.template.html',context_instance=RequestContext(request))
                else:
                    messages = 'Lo sentimos, este usuario está en espera de activación'
                    return render_to_response('base.login.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
            else:
                messages = 'Lo sentimos, el usuario o la contraseña no son válidos. Vuelve a intentarlo.'
                return render_to_response('base.login.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
    else:
        form = AuthenticationForm()
    return render_to_response('base.login.html', {'form': form}, context_instance=RequestContext(request))


def logout_view(request):
    """
    Función que permite cerrar la sesión del usuario
    Autor: Hugo Ramírez (hramirez@cenditel.gob.ve)
    Fecha: 2016
    """
    user = request.user
    if user.is_authenticated():
        logout(request)
    return redirect(reverse('login'))


def registro_usuario(request):
    """
    Función que permite crear usuarios del sistema, en espera de activación.
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 14-02-2017
    """
    usuario = request.user
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            messages = '¡Registro exitoso! debe esperar la activación de su cuenta'
            return render_to_response('base.login.html', {'messages': messages}, context_instance=RequestContext(request))
    args = {}
    args['form'] = UserForm
    return render(request, 'registro.html', args)


def edit_profile(request, pk):
    """
    Función que permite editar el perfil del usuarios autenticado.
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 20-03-2017
    """
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'GET':
        form = EditProfileForm(instance=user)
    else:
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        messages = '¡Perfil actualizado!'
        return render_to_response('user_profile.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
    return render(request, 'user_profile.html', {'form':form})

        
def useractive(request):
    users = User.objects.order_by('-pk')
    return render(request, 'admin.template.html', {"users": users})


def changestatus(request):
    """
    Funcion que activa, desactiva usuario y envia correo de confirmación
    Autor: Yngris Ibarguen (yibarguen@cenditel.gob.ve)
    Fecha: 2016
    Modificado: 2017
    """
    if request.method == 'POST':
        #obtengo el id del usuario 
        usuario = request.POST['idusuario']
        try:
            Usuario = User.objects.get(pk=usuario)
        except User.DoesNotExist:
            Usuario = None
        if (Usuario != None):
            if Usuario.is_active:
                Usuario.is_active = False
            else:
                Usuario.is_active = True
            dat_user = Usuario
            dat_user.save()
            
            if Usuario.is_active:
                email_subject = 'Cuenta activada'
                to_email = dat_user.email
                email_body = loader.get_template('mensaje-activacion.html').render(dict({'dat_user': dat_user}))
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER,
                [to_email], fail_silently=False)
            else:
                email_subject = 'Cuenta desactivada'
                to_email = dat_user.email
                email_body = loader.get_template('mensaje-desactivacion.html').render(dict({'dat_user': dat_user}))
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER,
                [to_email], fail_silently=False)

    return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))


def update_profile(request):
    if request.method == 'POST':
        #user_form = User.objects.get(pk=user_id)
        user_form = UserForm(request.POST['idusuario'])
       # user_form = request.POST['idusuario'] 
        profile_form = PerfilForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Tu perfil ha sido actualizado!'))
            return redirect('base:inicio')
        else:
            messages.error(request, ('Ocurrió un error.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = PerfilForm(instance=request.user.profile)
    return render(request, 'perfil.html', {'user_form': user_form, 'profile_form': profile_form}) 


def editar_contrasena(request):
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages = '¡La contraseña ha sido actualizada con exito!'
            return render(request, 'base.login.html', {'messages': messages}, context_instance=RequestContext(request))
    else:
        args = {}
        args['form'] = EditarContrasenaForm
    return render(request, 'base.password.html', args)


class UsuarioEliminar(SuccessMessageMixin,DeleteView):
    """
    Clase que permite eliminar un objeto(usuario) pidiendo confirmación por template
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 04-05-2017
    **************************
    ***** Aún en pruebas *****
    **************************
    """
    model = User
    #fields = ['username', 'last_name', 'email']
    success_url = reverse_lazy('base')
    success_message = "Se eliminó el usuario con éxito"