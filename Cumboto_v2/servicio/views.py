# Create your views here.
# -*- coding: utf-8 -*-
"""###################################################################################################
    #   ######## #####      ###              ###   #####  ##       #  #####  ###### ###### ########   #
    #      ##    ##   ##  ##   ##          ##   ## ##   # ##      #   ##   # ##     ##        ##      #
    #      ##    ##    ## #######  ######  ####### #####  ##     #    #####  ####   ######    ##      #
    #      ##    ##    ## ##   ##          ##   ## ##     ##    #     ##  ## ##         ##    ##      #
    #      ##    #####    ##   ##          ##   ## ##     ##   #      ##  ## ###### ######    ##      #
    ###################################################################################################"""

"""
Sistema para transmisión de aplicaciones desde las salas de control maestro de TV (CUMBOTO)

Copyleft (@) 2016 CENDITEL nodo Mérida - https://cumaco.cenditel.gob.ve/desarrollo/wiki/ftransporte
"""
## @namespace capa.views
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para las vistas del módulo de servicios
# @author Hugo Ramirez (hramirez at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import servicioModel
from .forms import servicioForm
#from capa.serializer import appSerializer
import json
import sys
import re
import ocumare
from ocumare.lutheria import tsco
#from ocumare.listar import listar
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .models import servicioModel
from .forms import servicioForm, SelectForm

###################################################
#             REST-FRAMEWORK CUMBOTO              #
###################################################

class servicioView(CreateView):

    """!
    Clase que permite almacenar los datos solicitados al servidor
    @author Hramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-06-2016
    """

    model = servicioModel
    form_class = servicioForm
    template_name = 'maquinaria.equipo.base.html'
    success_url = reverse_lazy('equipos')

    def form_valid(self, form):


        self.object = form.save(commit=False)
        self.object.servicio = form.cleaned_data['servicio']
        self.object.ranura = form.cleaned_data['ranura']
        self.object.codigo_app = form.cleaned_data['codigo_app']
        self.object.modalidad = form.cleaned_data['modalidad']
        self.object.save()

        return super(servicioView, self).form_valid(form)

def tst(request):
    if request.method == 'GET':
        form = servicioForm()
        return render(request, 'base.config.servicio.html', {'form': form})

@api_view(['POST' ,'GET'])
def GLOBAL_REST_FRAMEWORK(request):
    if request.method == 'GET':
        form = servicioForm()
        return render(request, 'base.servicio.html', {'form': form})

    if request.method == 'POST':
        form = servicioForm(request.POST)
        if form.is_valid():

            dtn = (form.cleaned_data['detener'])
            serv = (form.cleaned_data['servicio'])

            if serv == 'servicio_0':
                sv = int(0)
                print(sv)
            elif serv == 'servicio_1':
                sv = int(1)
                print(sv)
            elif serv == 'servicio_2':
                sv = int(2)
                print(sv)
            elif serv == 'servicio_3':
                sv = int(3)
                print(sv)
            elif serv == 'servicio_3':
                sv = int(4)
                print(sv)

            app = (form.cleaned_data['ranura'])
            cod = form.cleaned_data['codigo_app']
            ctl = form.cleaned_data['modalidad']


            if(dtn == "False"):
                servicio = sv
                ranura = int(app, 0)
                octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
                stop = octs.detener_ranura(servicio, ranura)
                stp = str(stop)
                success_message = "éxito"
                return Response(stp)
            else:
                if(dtn == "True"):
                    nv_edo = {
                    'serv': sv,
                    'app':  int(app, 0),
                    'cod':  cod,
                    'ctl':  int(ctl, 0),
                    }
                    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)
                    txt = str(octs)
                    return Response(txt)
        else:
            form = servicioForm()
            return render(request, 'base.servicio.html', {'form': form})
    else:
            form = servicioForm()
            return render(request, 'base.servicio.html', {'form': form})

###################################################
#             REST-FRAMEWORK CUMBOTO              #
###################################################

@api_view(['GET'])
def check(request, accion, codigo_apps):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    if accion == 'check_app':
        chk_app = octs.check_app(codigo_apps)
        return Response(chk_app)

    elif accion == 'check_edo':
        valid = octs.check_app(codigo_apps)
        if valid == False:
            return Response(valid)
        else:
            chk_edo = octs.check_edo(codigo_apps)
            return Response(chk_edo)

    elif accion == 'eliminar':
        if (octs.check_app(codigo_apps)) == True:
            delete = octs.eliminar_app(codigo_apps)
            return Response(delete)
        else:
            return Response(False)

###################################################
#             REST-FRAMEWORK CUMBOTO              #
###################################################

"""@api_view(['GET'])
def listar_elementos(request, accion_list):
    if accion_list == 'listar':
        lst = ocumare.listar.listar('/etc/cumaco/ocumare.conf')
        obt = lst.obtener_md()
        rest = str(obt)
        #list_json = json.loads(rest)
        return Response(rest)
    else:
        if accion_list == 'obt_lista_servicios':
            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
            list_serv = octs.obt_serv_md()
            #js = json.loads(list_serv)
            return Response(list_serv)"""

####################################################
#             REST-FRAMEWORK CUMBOTO               #
####################################################

@api_view(['GET'])
def copiar_apps(request, accion, cod, ruta):
    if accion == 'copiar':
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        octs.bib_copiar_app(cod)
        return Response("La Aplicacion Fue Copiada Con Exito")

####################################################
#             REST-FRAMEWORK CUMBOTO               #
####################################################

@api_view(['GET'])
def detener_serv(request, accion_det, serv, app):
    servicio = int(serv, 0)
    ranura = int(app, 0)
    if accion_det == 'detener':
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        stop = octs.detener_ranura(servicio, ranura)
        print(stop)
        stp = str(stop)
        return Response(stp)

####################################################
#             REST-FRAMEWORK CUMBOTO               #
####################################################

@api_view(['GET'])
def listar_servicios(request, accion_serv):
    if accion_serv == 'obt_lista_servicios':
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        list_serv = octs.obt_serv_md()
        return Response(list_serv)

####################################################
#             REST-FRAMEWORK CUMBOTO               #
####################################################

@api_view(['GET'])
def Obt_ranuras(request, accion_rns, serv):
    if accion_rns == 'obt_edo_ranuras':
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        print(serv)
        rs_ctl = octs.obt_edo_ranuras(serv)
        print(rs_ctl)
        return Response(rs_ctl)

@api_view(['POST' ,'GET'])
def REST_FRAMEWORK_CONSULT(request):

    if request.method == 'GET':
        return render(request, 'base.config.servicio.html')

    if request.method == 'POST':
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        lst = octs.obt_serv_md()
        a = type(lst)
        b = len(lst)
        for x in lst:
            return Response(lst)
    else:
        return render(request, 'base.config.servicio.html')

@api_view(['POST' ,'GET'])
def CONSULT_REST(request):

    if request.method == 'GET':
        form = SelectForm()
        return render(request, 'base.config.servicio.html', {'form': form})

    if request.method == 'POST':
        form = SelectForm(request.POST)
        if form.is_valid():
            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
            servicio = form.cleaned_data['select_serv']

            if servicio == 'servicio_0':
                sv = int(0)
            elif servicio == 'servicio_1':
                sv = int(1)
            elif servicio == 'servicio_2':
                sv = int(2)
            elif servicio == 'servicio_3':
                sv = int(3)
            elif servicio == 'servicio_3':
                sv = int(4)

            opciones = octs.obt_edo_ranuras(sv)
            op = ()
            for count in opciones:
                op += (count['control'], count['codigo'])
            print(op)
            n = opciones[0]
            m = opciones[1]
            for md in n, m:
                print(md.keys())
                #print(md.values())
            return Response(opciones)
        else:
            form = SelectForm()
            return render(request, 'base.config.servicio.html', {'form': form})
    else:
        form = SelectForm()
        return render(request, 'base.config.servicio.html', {'form': form})


class SELECT_VIEW(FormView):

    template_name = 'base.config.servicio.html'
    form_class = SelectForm
    success_url = 'servicio/consult/'

    def form_valid(self, form):
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        servicio = form.cleaned_data['select_serv']

        if servicio == 'servicio_0':
            sv = int(0)
        elif servicio == 'servicio_1':
            sv = int(1)
        elif servicio == 'servicio_2':
            sv = int(2)
        elif servicio == 'servicio_3':
            sv = int(3)
        elif servicio == 'servicio_3':
            sv = int(4)

        opciones = octs.obt_edo_ranuras(sv)
        opc = str(opciones)
        return Response(opc)

class index(TemplateView):
    emplate_name = 'base.config.servicio.html'

    def get(self,request):
        form = servicioForm()
        return render(request,self.template_name, {'form': form})
