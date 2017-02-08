#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,  render_to_response
from django.template import loader, Context,  RequestContext
from django.core.urlresolvers import reverse_lazy



@login_required
def inicio(request):
    return render_to_response('home.template.html', {}, context_instance=RequestContext(request))