from __future__ import unicode_literals
from django.conf.urls import url, patterns
from base.views import home
from base import views 


urlpatterns = [
	#url(r'^home/', home, name='home'),
	url(r'^$', views.home, name='home'),
]

