#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url, patterns
from usuario.forms import LoginForm
from django.contrib.auth.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

#inclusión del nombre del metodo login
from usuario.views import (
	changestatus, useractive, update_profile, acceso
   )
from . import views 

app_name = 'usuario'

urlpatterns = [
    url(r'^login/$', views.acceso, name='acceso'),
	#url(r'^login/$', views.login_view, name='login'),
	url(r'^registro/$', views.registro_usuario, name="registro"),
	url(r'^profile/$', views.Profile, name='perfil'),
	url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^adminuser/$', login_required(useractive), name='adminuser'),
    url(r'^changestatus/', login_required(changestatus), name='changestatus'),
    url(r'^password/$', login_required(views.editar_contrasena), name='editar_contrasena'),
    
    url(r'^reset/password_reset/$', password_reset, {'template_name': 'password_reset_form.html', 
        'email_template_name':'password_reset_email.html'},
        name='password_reset'),
    
    url(r'^password_reset/done/$', password_reset_done, {'template_name': 'password_reset_done.html'}, 
        name='password_reset/done/'),
   
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 
        password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, 
        name='password_reset_confirm'),
    
    url(r'^reset/done', password_reset_complete, {'template_name': 'password_reset_complete.html'}, 
        name='password_reset_complete'),
]
