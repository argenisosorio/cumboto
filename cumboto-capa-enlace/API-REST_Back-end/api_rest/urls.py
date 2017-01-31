"""api_rest URL Configuration
"""
from django.conf.urls import *
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api_rest/', include('capa.urls', namespace='api')),
]
