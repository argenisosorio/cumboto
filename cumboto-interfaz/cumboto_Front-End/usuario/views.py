# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context,  RequestContext
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.views.generic import TemplateView, FormView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import urlresolvers
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages.storage.cookie import CookieStorage
from django.views.generic import TemplateView, CreateView, ListView
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template import loader, Context
from django.views import generic
from django.views.generic import DeleteView
import logging
from django.contrib.auth import forms, login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator
logger = logging.getLogger("usuario")
from datetime import datetime
from .models import Perfil, Bitacora


class IndexTemplate(TemplateView):
   template_name = "home.template"


def acceso(request):
    """
    Función que gestiona la autenticación de los usuarios, maneja estatus de no logeado, inactivo en espera de activación y sin usuario creado.
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 13-02-2017
    """
    #if not request.user.is_anonymous():
        #return render_to_response('base.login.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    Bitacora.objects.create(usuario=request.user, descripcion='Accedio al sistema', tipo='Acceso', fecha_hora=datetime.now())
                    return render_to_response('home.template.html', context_instance=RequestContext(request))
                else:
                    messages = ['Lo sentimos, este usuario está en espera de activación']
                    return render_to_response('base.login.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
            else:
                messages = ['Lo sentimos, el usuario o la contraseña no son válidos. Vuelve a intentarlo.']
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


class UsuarioCreate(SuccessMessageMixin,CreateView):
    """
    Clase que registra los usuarios del sistema
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 22-05-2017
    """
    model = User
    form_class = UserForm
    template_name = "registro.html"
    success_url = reverse_lazy('usuario:acceso')
    success_message = "¡Registro exitoso! debe esperar la activacion de su cuenta"

    def form_valid(self,form):
        """
        Método que verifica si el formulario es válido, en cuyo caso procede a registrar los datos del usuario.
        Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
        Fecha: 22-05-2017
        """
        self.object = form.save(commit=False)
        self.object.username = form.cleaned_data['username']
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.set_password(form.cleaned_data['password1'])
        self.object.email = form.cleaned_data['email']
        self.object.is_active = 0
        self.object.save()

        # Registro de los campos extra del perfil del usuario
        perfil = Perfil()
        perfil.cargo = form.cleaned_data['cargo']
        perfil.user = self.object
        perfil.save()

        return super(UsuarioCreate, self).form_valid(form)


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
        Bitacora.objects.create(usuario=request.user, descripcion='Actualizó el perfil', tipo='Actualización', fecha_hora=datetime.now())
        return render_to_response('user_profile.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
    return render(request, 'user_profile.html', {'form':form})


def useractive(request):
    users = User.objects.order_by('-pk')
    if request.user.is_superuser:
        return render(request, 'admin.template.html', {"users": users})
    else:
        return render_to_response('home.template.html',context_instance=RequestContext(request))


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

def deleteusers(request):
    users = User.objects.order_by('-pk')
    if request.user.is_superuser:
        return render(request, 'admin.deleteusers.html', {"users": users})
    else:
        return render_to_response('home.template.html',context_instance=RequestContext(request))

def editusers(request):
    users = User.objects.order_by('-pk')
    if request.user.is_superuser:
        return render(request, 'admin.editusers.html', {"users": users})
    else:
        return render_to_response('home.template.html',context_instance=RequestContext(request))

def editclav(request):
    users = User.objects.order_by('-pk')
    if request.user.is_superuser:
        return render(request, 'admin.editclave.html', {"users": users})
    else:
        return render_to_response('home.template.html',context_instance=RequestContext(request))

def deluser(request):
    """
    Función que elimina un usuario y avisa por correo.
    Autor: Etzel Mencias
    Fecha: Mayo 2017
    """
    if request.method == 'POST':
        usuario = request.POST['idusuario']
        try:
            Usuario = User.objects.get(pk=usuario)
        except User.DoesNotExist:
            Usuario = None
        if (Usuario != None):
            dat_user = Usuario
            dat_user.save()
            email_subject = 'Cuenta eliminada'
            to_email = dat_user.email
            email_body = loader.get_template('mensaje-eliminacion.html').render(dict({'dat_user': dat_user}))
            send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)
            Usuario.delete()
    return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))

def ediuserone(request):
    """
    Función 01 para editar el correo.
    Autor: Etzel Mencias
    Fecha: Mayo 2017
    """
    if request.method == 'POST':
        idus = request.POST['idusuario']
        try:
            Usuario = User.objects.get(pk=idus)
        except User.DoesNotExist:
            Usuario = None
        if(Usuario != None):
            form = EditProfileForm(instance=Usuario)
            return render(request, 'editprofileone.html', {'form': form, 'idus': idus})
        else:
            return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))

def ediusertwo(request):
    """
    Función 02 para editar el correo.
    Autor: Etzel Mencias
    Fecha: Mayo 2017
    """
    if request.method == 'POST':
        idus = request.POST['idusuario']
        try:
            Usuario = User.objects.get(pk=idus)
        except User.DoesNotExist:
            Usuario = None
        if(Usuario != None):
            newemail = request.POST['email']
            username = request.POST['username']
            existe = User.objects.filter(email=newemail).exclude(username=username)
            if existe:
                raise forms.ValidationError('Ya existe un email igual en la Base de Datos.')
            Usuario.email = newemail
            Usuario.save()
            form = EditProfileForm(instance=Usuario)
            messages = '¡Email de usuario actualizado!'
            return render_to_response('editprofiletwo.html', {'form': form, 'messages': messages, 'idus': idus}, 
            context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))

def ediclavone(request):
    """
    Función 01 para editar la contraseña de un usuario.
    Autor: Etzel Mencias
    Fecha: Junio 2017
    """
    if request.method == 'POST':
        idus = request.POST['idusuario']
        try:
            Usuario = User.objects.get(pk=idus)
        except User.DoesNotExist:
            Usuario = None
        if(Usuario != None):
            form = EditClaveForm(instance=Usuario)
            return render(request, 'editclaveone.html', {'form': form, 'idus': idus})
        else:
            return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))

def ediclavtwo(request):
    """
    Función 02 para editar la contraseña de un usuario.
    Autor: Etzel Mencias
    Fecha: Junio 2017
    """
    if request.method == 'POST':
        idus = request.POST['idusuario']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        try:
            Usuario = User.objects.get(pk=idus)
        except User.DoesNotExist:
            Usuario = None
        if(Usuario != None):
            username = Usuario.username
            if(pass1 == pass2):
                form = EditClaveForm(request.POST, instance=Usuario)
                if form.is_valid():
                    Usuario.password = make_password(form.cleaned_data['password1'])
                    Usuario.save()
                    messages = '¡El cambio de contraseña ha sido exitoso!'
            else:
                messages = '¡Las contraseñas no coinciden, inténtelo de nuevo!'
            return render_to_response('editclavetwo.html', {'messages': messages, 'username': username, 'idus': idus}, 
                context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('usuario:adminuser'))


def change_password(request):
    """
    Funcion que cambia la contraseña del usuario.
    Autor: Yngris Ibarguen (yibarguen@cenditel.gob.ve)
    Fecha: 2016
    Modificado: Septiembre de 2017
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['new_password1'])
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, ('¡La contraseña ha sido actualizada con exito!'))
            return HttpResponseRedirect(urlresolvers.reverse('usuario:acceso'))

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base.password.html', {
        'form': form
    })


class BitacoraView(ListView):
    """
    Clase que muestra la lista de entradas de la bitácora
    Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
    Fecha: 06-07-2017
    """
    model = Bitacora
    template_name = "bitacora.html"

    def get(self, request, *args, **kwargs):
        """
        Método en el que definimos si un usaurio tiene permisos para acceder a la bitácora
        Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
        Fecha: 06-07-2017
        """
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        if request.user.is_superuser:
            return self.render_to_response(context)
        else:
            return render_to_response('home.template.html',context_instance=RequestContext(request))

    def get_queryset(self):
        """
        Método que filtra los datos de la tabla.
        Autor: Argenis Osorio (aosorio@cenditel.gob.ve)
        Fecha: 28-08-2017
        """
        #queryset = Bitacora.objects.filter(tipo='Acceso')
        queryset = Bitacora.objects.all()
        print "------"
        print queryset
        return queryset
