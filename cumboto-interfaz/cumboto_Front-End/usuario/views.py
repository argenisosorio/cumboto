# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context,  RequestContext
from django.contrib.auth.models import User
from .forms import UserForm, LoginForm, EditarEmailForm, EditarContrasenaForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import urlresolvers
from django.contrib import messages
import logging
logger = logging.getLogger("usuario")

def acceso(request):
   
    form = AuthenticationForm()


    if request.method == "POST":

        username = request.POST.get('username')
        if not User.objects.filter(username=username):
            messages = 'Lo sentimos, El usuario o la contraseña no son válidos. Vuelve a intentarlo.'
            return render_to_response('base.login.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
        
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            usuario = authenticate(username=username, password=str(password))

            if usuario is not None:
                login(request, usuario)
                usr = User.objects.get(username=username)
                usr.save()
            else:
                messages = 'Lo sentimos, El usuario o la contraseña no son válidos. Vuelve a intentarlo.'
                return render_to_response('base.login.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
                #logger.error(str(_("Error al autenticar el usuario [%s]") % username))

            logger.info(str(_("Acceso al sistema por el usuario [%s]") % username))
            return HttpResponseRedirect(urlresolvers.reverse("base:inicio"))

    return render_to_response('base.login.html', {'form': form}, context_instance=RequestContext(request))


def logout_view(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
    return redirect(reverse('login'))


def useractive(request):

    users = User.objects.order_by('-pk')
    return render_to_response('admin.template.html', {"users": users},context_instance=RequestContext(request))


class registro_usuario_view(FormView):
    template_name = 'registro.html'
    form_class = UserForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        return super(registro_usuario_view, self).form_valid(form)

#Cambiar estatus de los usuarios
def changestatus(request):
    if request.method == 'POST':
        #obtengo el id del usuario 
        usuario = request.POST['idusuario'] 
        print (usuario)
        try:
            Usuario = User.objects.get(pk=usuario)
        except User.DoesNotExist:
            Usuario = None
        if (Usuario != None):
            if Usuario.is_active:
                Usuario.is_active = False
            else:
                Usuario.is_active = True
            Usuario.save()
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
            messages.success(request, 'La contraseña ha sido cambiado con exito!.')
            messages.success(request, 'Es necesario introducir los datos para entrar.')
            return redirect(reverse('base:inicio'))
    else:
        form = EditarContrasenaForm()
    return render(request, 'base.password.html', {'form': form}) 