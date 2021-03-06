#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, patterns
from usuario.forms import LoginForm
from django.contrib.auth.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import PasswordResetForm
from .views import *
from . import views
from usuario.views import *

app_name = 'usuario'

urlpatterns = [
    url(r'^login/$', views.acceso, name='acceso'),
    url(r'^bienvenido/$', login_required(inicio), name='inicio'),
    url(r'^crear_usuario/$', UsuarioCreate.as_view(), name='registro'),
    url(r'^perfil/(?P<pk>\d+)$', login_required(views.edit_profile), name="perfil"),
    url(r'^bitacora', login_required(views.BitacoraView.as_view()), name='bitacora'),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^adminuser/$', login_required(useractive), name='adminuser'),
    url(r'^changestatus/', login_required(changestatus), name='changestatus'),
    url(r'^admdelusers/$', login_required(deleteusers), name='admdelusers'),
    url(r'^admedusers/$', login_required(editusers), name='admedusers'),
    url(r'^admedclav/$', login_required(editclav), name='admedclav'),
    url(r'^deluser/$', login_required(deluser), name='deluser'),
    url(r'^ediuserone/$', login_required(ediuserone), name='ediuserone'),
    url(r'^ediusertwo/$', login_required(ediusertwo), name='ediusertwo'),
    url(r'^ediclavone/$', login_required(ediclavone), name='ediclavone'),
    url(r'^ediclavtwo/$', login_required(ediclavtwo), name='ediclavtwo'),
    url(r'^password/$', login_required(views.change_password), name='change_password'),
    url(r'^reset/password_reset/$', password_reset, {'template_name': 'password_reset_form.html', 
        'email_template_name':'password_reset_email.html', 'password_reset_form':PasswordResetForm},
        name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, {'template_name': 'password_reset_done.html'}, 
        name='password_reset/done/'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 
        password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, 
        name='password_reset_confirm'),
    url(r'^reset/done', password_reset_complete, {'template_name': 'password_reset_complete.html'}, 
        name='password_reset_complete'),
]
