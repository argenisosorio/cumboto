from __future__ import unicode_literals
from django.conf.urls import url, patterns
from .views import registrar_view, metadatos_get_data, listar_app_view, ListDataJsonView, zip_get_data, delete_get_data
from django.contrib.auth.decorators import login_required

app_name = 'biblioteca'


urlpatterns = [
	url(r'^biblioteca$', login_required(registrar_view.as_view()), name="subir"),
	url(r'^biblioteca/listar$', login_required(listar_app_view), name="listar"),
	url(r'^biblioteca/data$', login_required(ListDataJsonView.as_view()), name="listar_data"),
]

# Urls usadas para ajax
urlpatterns += [
    url(r'^ajax/metadatos-data$', login_required(metadatos_get_data) ,name="metadatos_data"),
    url(r'^biblioteca/ajax/delete-data$', login_required(delete_get_data) ,name="delete_data"),
    url(r'^ajax/enviar-zip$', login_required(zip_get_data) ,name="enviar_zip_data"),
]