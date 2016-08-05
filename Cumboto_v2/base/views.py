# -*- coding: utf-8 -*-
"""
 Sistema para transmisión de aplicaciones desde las salas de control maestro de TV (CUMBOTO)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://cumaco.cenditel.gob.ve/desarrollo/browser/cumboto/Cumboto_v2
"""
## @namespace base.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo base
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def inicio(request):
    """!
    Función que permite cargar la pantalla de inicio del sistema

    @author hramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 01-08-2016
    @param request <b>{object}</b> Objeto que obtiene la petición
    @return Devuelve el response con la página de inicio del sistema
    """
    return render_to_response('base.template.html', {}, context_instance=RequestContext(request))