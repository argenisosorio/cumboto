from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context,  RequestContext
from django.contrib.auth.models import User
from .forms import UserForm, LoginForm, EditarEmailForm, EditarContrasenaForm,  ProfileForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.core import urlresolvers
from django.contrib import messages
import datetime
from usuario.models import Profile


def login_view(request):
    message = None
    if request.user.is_authenticated():
        return redirect(reverse('base:home'))
    if request.method == 'POST':
        user = AuthenticationForm(request.POST)
        if user.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    message ="Has iniciado sesión de manera correcta"
                    return redirect(reverse('base:home'))
                else: 
                    message ="Tu usuario esta inactivo"
            else: 
                message ="Nombre de usuario y/o password incorrecto"
    else:
        form = AuthenticationForm()
    return render_to_response('login.html', {'message': message, 'form':form}, context_instance=RequestContext(request))


def logout_view(request):
	user = request.user
	if user.is_authenticated():
		logout(request)
	return HttpResponseRedirect(urlresolvers.reverse('login'))


def useractive(request):
    # - es desc, quitar para ordernar asc
    users = User.objects.order_by('-pk') #.all()
    return render_to_response('admin.html', {"users": users},context_instance=RequestContext(request))

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



class registro_usuario_view(FormView):
    template_name = 'registro.html'
    form_class = UserForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        #perfil = Perfiles()
        #perfil.usuario = user
        #perfil.telefono = form.cleaned_data['telefono']
        #perfil.save()
        return super(registro_usuario_view, self).form_valid(form)



def update_profile(request):
    if request.method == 'POST':
        #user_form = User.objects.get(pk=user_id)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Tu perfil ha sido actualizado!'))
            return redirect('base:home')
        else:
            messages.error(request, ('Ocurrió un error.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'perfil.html', {
                    'user_form': user_form, 
                    'profile_form': profile_form}, 
                    context_instance=RequestContext(request))







'''
def adminperfiles(request):
    users = UserProfile.objects.get()
    return render_to_response('perfil.html', {"users": users}, context_instance=RequestContext(request))


def editar_email(request):
    if request.method == 'POST':
        form = EditarEmailForm(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'El email ha sido cambiado con exito!.')
            return redirect(reverse('base:home'))
    else:
        form = EditarEmailForm(
            request=request,
            initial={'email': request.user.email})
    return render(request, 'editar_email.html', {'form': form})   
'''

#@login_required
def editar_contrasena(request):
    if request.method == 'POST':
        form = EditarContrasenaForm(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, 'La contraseña ha sido cambiado con exito!.')
            messages.success(request, 'Es necesario introducir los datos para entrar.')
            return redirect(reverse('base:home'))
    else:
        form = EditarContrasenaForm()
    return render(request, 'editar_contrasena.html', {'form': form}) 
