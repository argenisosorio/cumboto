# -*- coding: utf-8 -*-
"""api_rest URL Configuration
"""
from django.conf.urls import *
from django.contrib import admin

from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

from capa import views

router = routers.DefaultRouter()
router.register(r'archivo', views.ArchivoVerSet)

urlpatterns = [
    url(r'^',include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api_rest/', include('capa.urls', namespace='api')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
