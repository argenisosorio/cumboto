# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from django.views.generic import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from .models import appModel
from .forms import appForm
from capa.serializer import appSerializer
import json
import sys
import re, os
sys.path.append('/usr/local/src/ocumare/luth/')
import ocumare.lutheria
#import ocumare	
import base64
#import gnupg
import zipfile
#from ocumare.listar import listar
#from ocumare.lutheria import tsco
from django.views.generic import CreateView
from django.http import HttpResponse

from .models import Archivo
from rest_framework import viewsets
from rest_framework import filters
from serializer import appSerializer 

@api_view(['POST'])
def add_app(request):
    if request.method == 'POST':
        form = appForm(request.POST)
        if form.is_valid():
            serv = (form.cleaned_data['servicio'])
            app = (form.cleaned_data['ranura'])
            cod = (form.cleaned_data['codigo_app'])
            ctl = (form.cleaned_data['modalidad'])

            octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
            rest = octs.check_app(form.cleaned_data['codigo_app'])
            if rest == True:

                nv_edo = {
                    'serv':	serv,
                    'app':	app,
                    'cod':	cod,
                    'ctl':	ctl,
                }
                new_edo = octs.nv_edoc(nv_edo)
                print (new_edo)
                #nv = str(new_edo)
                return Response(new_edo)
                #return Response(True)

            #if(octs.check_app(form.cleaned_data['codigo_app'])) == False:
             #   return Response(False)
        else:
            form = appForm()
            return render(request, 'index.html', {'form': form})


@api_view(['POST'])
def validator_app(request):
    if request.method == 'POST':
        form = appForm(request.POST)
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
                return Response(nv_edo)

        else:
            form = appForm()
            return render(request, 'index.html', {'form': form})


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


@api_view(['GET'])
def check_edo_app(request,codigo_apps):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    chk_edo = octs.check_edo(codigo_apps)
    print(str(chk_edo))
    return Response(chk_edo)
    

@api_view(['GET'])
def checked_aplicacion(request, codigo_apps):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    ck_app = octs.check_app(codigo_apps)
    return Response(ck_app)


@api_view(['GET'])
def eliminar_app(request,codigo_apps):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    exist = octs.check_app(codigo_apps)
    if exist == True:
        delete = octs.eliminar_app(codigo_apps)
        message = 'La Aplicacion Fue Eliminada'
        return Response(message)
    else:
        message = 'La Aplicacion Solicitada No Existe'
        return Response(message)


@api_view(['GET'])
def nuevo_edo_app(request,serv,app,cod,ctl):
    
    if serv == 'servicio_0':
        sv = int(0)
    elif serv == 'servicio_1':
        sv = int(1)
    elif serv == 'servicio_2':
        sv = int(2)
    elif serv == 'servicio_3':
        sv = int(3)
    elif serv == 'servicio_4':
        sv = int(4)

    try:

        nv_edo = {
                'serv': sv,
                'app':  int(app, 0),
                'cod':  cod,
                'ctl':  int(ctl, 0),
                }
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf', nv_edo)

    except(RuntimeError, TypeError, NameError, ValueError, IOError):

        message = False
        return Response(message)      
    
    message = True
    return Response(message)


@api_view(['GET'])
def listar_elementos(request):

    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    lst = octs.obt_serv_md()
    data = json.dumps(lst)
    return Response(lst,status=None, template_name=None, headers=None, content_type=None)


@api_view(['GET'])
def copiar_apps(request):

    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    copy = request.get('http://127.0.0.1:8000/')
    octs.bib_copiar_app(cod)
    message = 'La Aplicacion Fue Copiada Con Exito'
    return Response(message)


@api_view(['GET'])
def detener_serv(request, serv, app):
    
    rn = int(app, 0)
    
    if serv == 'servicio_0':
        sv = int(0)
    elif serv == 'servicio_1':
        sv = int(1)
    elif serv == 'servicio_2':
        sv = int(2)
    elif serv == 'servicio_3':
        sv = int(3)
    elif serv == 'servicio_4':
        sv = int(4)
        
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    stop = octs.detener_ranura(sv, rn)
    stp = str(stop)
    return Response(stp)


@api_view(['GET'])
def listar_servicios(request, accion_serv):
    if accion_serv == 'obt_lista_servicios':
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        list_serv = octs.obt_serv_md()
        opciones = ()
        for x in list_serv:
            codigo = x['codigo']
            nombre = x['n']
            opciones += (x['codigo'],x['n']),
        return Response(codigo, nombre)


@api_view(['GET'])
def Obt_ranuras(request, serv):

        if serv == 'servicio_0':
            sv = int(0)
        elif serv == 'servicio_1':
            sv = int(1)
        elif serv == 'servicio_2':
            sv = int(2)
        elif serv == 'servicio_3':
            sv = int(3)
        elif serv == 'servicio_4':
            sv = int(4)

        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        opciones = octs.obt_edo_ranuras(sv)
        if opciones == None:
            message = 'Servicio Inactivo'
            return Response(message)
        else:
            return Response(opciones)

@api_view(['GET'])
def listar_aplicaciones(request):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    aplicaciones = octs.obt_apps_biblio()
    return Response(aplicaciones)


@api_view(['GET'])
def config_omision(request, cod):
    octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
    config_omision = octs.nv_edo_app_rell(cod)
    return Response(config_omision)


@api_view(['GET', 'POST'])
def decoded_zip(request, encoded):
    
    ### Object Decrytp ###
    if request.method == 'POST':
        decoded = base64.b64decode(encoded)
        print(decoded)
        octs = ocumare.lutheria.tsco('/etc/cumaco/ocumare.conf')
        copiar = octs.bib_copiar_app(decoded)

        return Response(copiar) 


class ArchivoVerSet(viewsets.ModelViewSet):
    """
    Clase que permite clasificar la información a serealizar
    Autor: Luis Guillermo Echenque (lechenique@gmail.com)
    fecha: 22-05-2017
    """
    queryset = Archivo.objects.all()
    serializer_class = appSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter,)
    filter_fields  = ('descomprimido',)
    ordering = ('fecha_creado',)
