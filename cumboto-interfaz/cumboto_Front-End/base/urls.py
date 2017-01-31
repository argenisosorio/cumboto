from __future__ import unicode_literals
from django.conf.urls import url, patterns
from base.views import inicio
from base import views 


urlpatterns = [
	url(r'^$', views.inicio, name='inicio'),
]

