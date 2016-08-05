
from __future__ import unicode_literals
from django.conf.urls import url
from .views import inicio

urlpatterns = [
    url(r'^inicio/$', 'base.views.inicio', name='inicio'),
]