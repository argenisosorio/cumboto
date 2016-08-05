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
from django.views.generic import ListView
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
from ocumare.listar import listar
from django.views.generic import CreateView
from django.http import HttpResponse


###################################################
#             REST-FRAMEWORK CUMBOTO              #
###################################################
class GLOBAL_REST_FRAMEWORK(CreateView):

    model = servicioModel
    form_class = servicioForm
    template_name = 'base.servicio.html'
    success_url = reverse_lazy('global')

    def post(request):
        if request.method == 'POST':
            form = servicioForm(request.POST)
            if form.is_valid():
                accion = form.cleaned_data['accion']
                serv = form.cleaned_data['servicio']
                app = form.cleaned_data['ranura']
                cod = form.cleaned_data['codigo_app']
                ctl = form.cleaned_data['modalidad']

                octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
                aplicacion = octs.check_app(form.cleaned_data['codigo_app'])
                if aplicacion == True:
                    nv_edo = {
                    'serv':	int(serv, 0),
                    'app':	int(app, 0),
                    'cod':	cod,
                    'ctl':	int(ctl, 0),
                    }
                    print(nv_edo)
                    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)
                    txt = str(octs)
                    print (octs)
                    return Response(txt)
            else:
                form = servicioForm()
                return render(request, 'base.servicio.html', {'form': form})
        else:
                form = servicioForm()
                return render(request, 'base.servicio.html', {'form': form})


class GLOBAL_REST(CreateView):

    model = servicioModel
    form_class = servicioForm
    template_name = 'base.servicios.html'

    @api_view(['POST'])
    def form_valid(self, form):

        self.object.acc = (form.cleaned_data['accion'])
        self.object.serv = (form.cleaned_data['servicio'])
        self.object.app = (form.cleaned_data['ranura'])
        self.object.cod = (form.cleaned_data['codigo_app'])
        self.object.ctl = (form.cleaned_data['modalidad'])

        print(self.object.form.cleaned_data['accion'])

        if self.object.acc == 'nuevo_edo':

            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
            aplicacion = octs.check_app(form.cleaned_data['codigo_app'])

            if aplicacion == True:
                nv_edo = {
                    'serv':	int(self.object.serv, 0),
                    'app':	int(self.object.app, 0),
                    'cod':	self.object.cod,
                    'ctl':	int(self.object.ctl, 0),
                }
                octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)
                txt = str(octs)
                print (octs)
                return Response(txt)

            else:
                if self.object.acc == 'detener':
                    servicio = int(self.object.serv, 0)
                    ranura = int(self.object.app, 0)
                    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
                    stop = octs.detener_ranura(servicio, ranura)
                    print(stop)
                    stp = str(stop)
                    return Response(stp)
                else:
                    form = servicioForm()
                    return render('base.servicios.html', {'form': form})
        else:
            form = servicioForm()
            return render('base.servicios.html', {'form': form})

    """def form_valid(self, form):
        self.object.accion = form.cleaned_data['accion']
        self.object.serv = form.cleaned_data['servicio']
        self.object.app = form.cleaned_data['ranura']
        self.object.cod = form.cleaned_data['codigo_app']
        self.object.ctl = form.cleaned_data['modalidad']
        if self.object.accion == 'nuevo_edo':
            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
            aplicacion = octs.check_app(form.cleaned_data['codigo_app'])
            if aplicacion == True:
                nv_edo = {
                    'serv':	int(self.object.serv, 0),
                    'app':	int(self.object.app, 0),
                    'cod':	self.object.cod,
                    'ctl':	int(self.object.ctl, 0),
                }
                octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)
                txt = str(octs)
                print (octs)
                return Response(txt)
            else:
                form = servicioForm()
                return render('index.html', {'form': form})
        else:
            if form.cleaned_data['accion'] == 'detener':
                servicio = int(self.object.serv, 0)
                ranura = int(self.object.app, 0)
                octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
                stop = octs.detener_ranura(servicio, ranura)
                print(stop)
                stp = str(stop)
                return Response(stp)
            else:
                form = servicioForm()
                return render('servicios.base.html', {'form': form})"""

########################################

@api_view(['POST' ,'GET'])
def add_app(request):
    if request.method == 'GET':
        form = servicioForm()
        return render(request, 'base.servicio.html', {'form': form})

    if request.method == 'POST':
        form = servicioForm(request.POST)
        if form.is_valid():

            dtn = (form.cleaned_data['detener'])
            serv = (form.cleaned_data['servicio'])
            app = (form.cleaned_data['ranura'])
            cod = form.cleaned_data['codigo_app']
            ctl = form.cleaned_data['modalidad']

            print(dtn)
            print(serv)
            print(app)
            print(cod)
            print(ctl)

            if(dtn == "False"):
                servicio = int(serv, 0)
                ranura = int(app, 0)
                octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
                stop = octs.detener_ranura(servicio, ranura)
                print(stop)
                stp = str(stop)
                print("detenido")
                return Response(stp)

            else:
                if(dtn == "True"):
                    nv_edo = {
                    'serv': int(serv, 0),
                    'app':  int(app, 0),
                    'cod':  cod,
                    'ctl':  int(ctl, 0),
                    }
                    print(nv_edo)
                    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)
                    txt = str(octs)
                    print (octs)
                    print("Nuevo Estado")
                    return Response(txt)




        else:
            form = servicioForm()
            return render(request, 'base.servicio.html', {'form': form})
    else:
            form = servicioForm()
            return render(request, 'base.servicio.html', {'form': form})

@api_view(['POST'])
def validator_app(request):
    if request.method == 'POST':
        form = servicioForm(request.POST)
        if form.is_valid():
            serv = (form.cleaned_data['servicio'])
            app = (form.cleaned_data['ranura'])
            cod = (form.cleaned_data['codigo_app'])
            ctl = (form.cleaned_data['modalidad'])
            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
            rest = octs.check_app(cod)
            if rest == True:
                nv_edo = {
                    'serv':	serv,
                    'app':	app,
                    'cod':	cod,
                    'ctl':	ctl,
                }
                print (nv_edo)
                chk_app = octs.check_app(cod)
                if chk_app == True:
                    chk_edo = octs.check_edo(cod)
                return Response(chk_edo)

        else:
            form = servicioForm()
            return render(request, 'servicios.base.html', {'form': form})

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

@api_view(['GET'])
def nuevo_edo_app(request,accion,serv,app,cod,ctl):

    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    if octs.check_app(cod) == True:
        print (ctl)
        print(serv)
        if accion == 'nuevo_edo':
            nv_edo = {
                'serv':	int(serv, 0),
                'app':	int(app, 0),
                'cod':	cod,
                'ctl':	int(ctl, 0),
            }
            """print type(cod)
            print (nv_edo)
            s = nv_edo['serv']
            sx = int(s)
            print type(sx)
            print (sx)
            print (s)
            print type(s)"""
            #tst = octs.gen_nvtsco(nv_edo)
            #carrusel = octs.gen_nv_carrusel(serv, app)
            #print (carrusel)
            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)
            #new_edo = octs.nv_edoc('/etc/cumaco/ocumare.conf', nv_edo)
            #print(new_edo)
            #new_edo = ocumare.lutheria.tsco.nv_edoc('/etc/cumaco/ocumare.conf', nv_edo)
            #print(new_edo)
            #nv = str(octs)
            #print(nv)
            result = str(octs)
            return Response(result)
    else:
        return Response(False)


###################################################
#             REST-FRAMEWORK CUMBOTO              #
###################################################

@api_view(['GET'])
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
            return Response(list_serv)

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
        print (serv)
        rs_ctl = octs.obt_edo_ranuras(serv)
        print (rs_ctl)
        return Response(rs_ctl)

