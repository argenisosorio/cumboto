# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from .views import GLOBAL_REST_FRAMEWORK, tst

urlpatterns = [
    #################################################################

    url(r'^global/',GLOBAL_REST_FRAMEWORK, name='global'),
    url(r'^global-tst/',tst, name='global-test'),

    #################################################################

]
