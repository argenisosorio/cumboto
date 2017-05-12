#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from base.views import inicio


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cumboto/', include('base.urls', namespace='base', app_name='base')),
    url(r'^$',inicio, name='inicio'),
    url(r'^cumboto/', include('usuario.urls')),
    url(r'^cumboto/', include('biblioteca.urls', namespace='biblioteca')),
    url(r'^cumboto/', include('servicio.urls', namespace='servicios')),
    #url(r'^', include('agenda.urls')),
    url(r'^cumboto/', include('django.contrib.auth.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
