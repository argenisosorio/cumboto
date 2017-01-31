# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from .views import *
urlpatterns = [

    #################################################################

    url(r'^servicios/configuracion',login_required(GLOBAL_REST_FRAMEWORK), name='global'),
    #url(r'^Tornado',login_required(consultar_rest), name='Tornado'),
    #url(r'^consulta',login_required(SELECT_VIEW.as_view()), name='consulta'),
    #url(r'^global-consult',login_required(REST_FRAMEWORK_CONSULT), name='global-consult'),
    url(r'^servicios/consulta-servicios',login_required(CONSULT_REST), name='rest_consulta'),
    url(r'^servicios/app-omision',login_required(configurar_omision), name='app_omision'),
    url(r'^servicios/data$', login_required(TableDataJsonView.as_view()), name="data_table"),

    #################################################################

]

# Urls usadas para ajax
urlpatterns += [
    url(r'^servicios/ajax/servicios-data$', login_required(servicios_get_data) ,name="servicios_data"),
    url(r'^servicios/ajax/aplicaciones-data$', login_required(aplicaciones_get_data) ,name="aplicaciones_data"),
    url(r'^servicios/ajax/ranuras-data$', login_required(ranuras_get_data) ,name="ranuras_data"),
    url(r'^servicios/ajax/correr-data$', login_required(correr_get_data) ,name="correr_data"),
    url(r'^servicios/ajax/detener-data$', login_required(detener_get_data) ,name="detener_data"),
    url(r'^servicios/ajax/config-omision-data$', login_required(omision_get_data) ,name="omision_data"),
]
