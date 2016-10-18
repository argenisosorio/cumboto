from __future__ import unicode_literals
from django.conf.urls import url, patterns
from usuario.forms import LoginForm
from django.contrib.auth import views as auth_views
from usuario.views import (
	registro_usuario_view, changestatus, useractive, update_profile, 
   )
from . import views

app_name = 'usuario'


urlpatterns = [
	url(r'^registro/$', registro_usuario_view.as_view(), name="registro"),
	url(r'^login/$', auth_views.login, {'template_name': 'login.html'}),
	url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^adminuser/$', useractive, name='adminuser'),
    url(r'^changestatus/', changestatus, name='changestatus'),
    url(r'^actualizar-perfil/$', views.update_profile, name='actualizar-perfil'),
    #url(r'^editar_email/$', views.editar_email, name='editar_email'),
    url(r'^editar_contrasena/$', views.editar_contrasena, name='editar_contrasena'),
]

