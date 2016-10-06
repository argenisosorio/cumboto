# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from .views import GLOBAL_REST_FRAMEWORK, REST_FRAMEWORK_CONSULT, SELECT_VIEW, CONSULT_REST

urlpatterns = [
    #################################################################

    url(r'^global/',GLOBAL_REST_FRAMEWORK, name='global'),
    url(r'^consult/',SELECT_VIEW.as_view(), name='consulta'),
    url(r'^global-consult/',REST_FRAMEWORK_CONSULT, name='global-consult'),
    url(r'^consulta-rest/',CONSULT_REST, name='rest-consult'),

    #################################################################

]
