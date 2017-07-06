#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Perfil, Bitacora

admin.site.register(Perfil)
admin.site.register(Bitacora)
