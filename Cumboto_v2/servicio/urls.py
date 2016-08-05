# -*- coding: utf-8 -*-
"""###################################################################################################
    #   ######## #####      ###              ###   #####  ##       #  #####  ###### ###### ########   #
    #      ##    ##   ##  ##   ##          ##   ## ##   # ##      #   ##   # ##     ##        ##      #
    #      ##    ##    ## #######  ######  ####### #####  ##     #    #####  ####   ######    ##      #
    #      ##    ##    ## ##   ##          ##   ## ##     ##    #     ##  ## ##         ##    ##      #
    #      ##    #####    ##   ##          ##   ## ##     ##   #      ##  ## ###### ######    ##      #
    ###################################################################################################"""

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.decorators import api_view
from django.utils.translation import ugettext_lazy as _
from .views import GLOBAL_REST_FRAMEWORK, GLOBAL_REST, validator_app, add_app
from django.views.generic import CreateView

urlpatterns = [

    url(r'^global/',GLOBAL_REST_FRAMEWORK.as_view(), name='global'),
    url(r'^inicio/',GLOBAL_REST.as_view(), name='inicio'),
    url(r'^add-app/',add_app, name='app'),
    url(r'^Framework-Rest/',validator_app, name='validator_app'),

    #################################################################

]
