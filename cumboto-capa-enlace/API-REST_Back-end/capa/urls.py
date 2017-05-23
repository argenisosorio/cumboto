# -*- coding: utf-8 -*-

from django.conf.urls import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.decorators import api_view
from django.utils.translation import ugettext_lazy as _
from .views import *
from django.views.generic import CreateView
from django.contrib import admin
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from capa import views

router = routers.DefaultRouter()
router.register(r'archivo', views.ArchivoVerSet)

urlpatterns = [

    url(r'^',include(router.urls)),
    url(r'^add-app/$',add_app, name='app'),
    url(r'^Framework-Rest/$',validator_app, name='validator_app'),
    #url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),

    url(r'^file/(?P<encoded>.+)$',decoded_zip, name='decoded'),
    #url(r'^file/',decoded_zip, name='decoded'),
    url(r'^accion/(?P<accion>.+)/codigo/(?P<codigo_apps>.+)$',check, name='check'),
    url(r'^checked_exists/(?P<codigo_apps>.+)$',checked_aplicacion, name='check_exists'),
    url(r'^checked_edo_app/(?P<codigo_apps>.+)$',check_edo_app, name='check_edo_app'),
    url(r'^eliminar/(?P<codigo_apps>.+)$',eliminar_app, name='eliminar'),
    url(r'nv_edo/(?P<serv>.+)/(?P<app>.+)/(?P<cod>.+)/(?P<ctl>.+)$',nuevo_edo_app, name='nv_edo'),
    #url(r'^listar/(?P<accion_list>.+)$',listar_elementos, name='obt_list'),
    url(r'^listar$',listar_elementos, name='obt_list'),
    url(r'^listar-aplicaciones$',listar_aplicaciones, name='listar_aplicaciones'),
    url(r'^copiar/(?P<accion>.+)/(?P<cod>.+)/(?P<ruta>.+)$',copiar_apps, name='cop_app'),
    url(r'^detener/(?P<serv>.+)/(?P<app>.+)$',detener_serv, name='detener_ranura'),
    url(r'^servicios/(?P<accion_serv>.+)$',listar_servicios, name='obt_list_serv'),
    url(r'^ranuras/(?P<serv>.+)$',Obt_ranuras, name='obt_list_ctl'),
    url(r'^omision/(?P<cod>.+)$',config_omision, name='omision'),
]
