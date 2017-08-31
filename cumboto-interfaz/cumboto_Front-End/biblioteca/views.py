# -*- coding: utf-8 -*-
import os , sys , codecs
import shutil
import zipfile
import re , configparser
import json
import requests
import random, struct
from django.conf import settings
from django.http import JsonResponse
from ConfigParser import ConfigParser
from django.shortcuts import render,  render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.contrib import messages
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView
from .forms import registrar_form
from .models import registrar_app, metadata_model
from django_datatables_view.base_datatable_view import BaseDatatableView
import base64
from django.core.exceptions import ValidationError
from django.core import urlresolvers


class registrar_view(CreateView):
    """
    Clase que permite registrar una aplicación en la biblioteca
    Autor: Hugo Ramírez (hramirez@cenditel.gob.ve)
    Fecha: 2016
    """
    template_name= 'registro.template.html'
    form_class = registrar_form
    success_url = reverse_lazy('biblioteca:subir')
    
    def valid_extension(value):
        if (not value.name.endswith('.zip')):
            raise ValidationError("Archivos permitidos: .zip")

    def encrypt(value):
        with open(value, "rb") as file_z:
            encoded = base64.b64encode(file_z.read())
            return True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.cargar_app = form.cleaned_data['cargar_app']
        self.object.save()        
        namefile = form.cleaned_data['cargar_app'].name
        FilePath =('tmp/'+namefile)
        folders = []
        try:
            z = zipfile.ZipFile(open(FilePath,"rb"))
            for name in z.namelist():
                z.extract(name)
                if(name[-1] == "/"):
                    folders.append(name)
                metadata = name

            ##### Metadatos #####

            #ruta del directorio
            path = os.getcwd()
            Eliminar_zip = path+'/'+FilePath
            
            #Lista vacia para incluir los ficheros
            lstFiles = []

            #Lista con todos los ficheros del directorio:
            lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros


            #Crea una lista de los ficheros conf que existen en el directorio y los incluye a la lista.
            #for root, dirs, files in lstDir:

                #for fichero in files:
                    #(nombreFichero, extension) = os.path.splitext(fichero)
                    
            metadata= name
            name_dir = os.path.dirname(metadata)
            ruta = path+'/'+name_dir

            ### Valida que exista el archivo metadatos.conf y el directorio aplicacion
            metadatos = os.path.isfile(os.path.join(ruta, 'metadatos.conf'))
            aplicacion = os.path.isdir(os.path.join(ruta, 'aplicacion'))

            if metadatos == True and aplicacion == True:
                ### Contenedor ###
                metadata = name

                #### Leer Diccionario ####
                def leerDict(diccionario, elemento):
                    for i, j in elemento.items():
                        diccionario = diccionario.replace(i, j)
                    return diccionario

                #### Limpieza ####
                def limpieza(l):
                    v = True
                    while v == True:
                        try:
                            c= l.index ('')
                        except ValueError:
                            c = -1
                            v= False
                        if c > 0:
                            c = l.remove ('')

                #### Parsear los Metadatos ####
                def parsearFile(metadata):
                    libreria=[]
                    parserFile = open(metadata, 'r').read()
                    p = parserFile.split('\n')
                    configP = configparser.RawConfigParser()
                    parse = r""+metadata+""
                    configP.readfp(codecs.open(parse, "r", "utf8"))
                    limpieza(p)
                    for parsemeta  in range (len(p)):
                        if parsemeta == 0:
                            elementos = {'[':'',']':''}
                            result = leerDict(p[0], elementos)
                        if parsemeta > 0:
                            indicadores = {':':'','=':''}
                            dictParser = leerDict(p[parsemeta], indicadores)
                            c= dictParser.split()
                            e = configP.get(result, c[0])
                            e = e.split()
                            libreria.append({c[0] : e[0]})
                    return libreria
            else:
                form = registrar_form
                msg_error = 'El archivo No cumple con los requeisitos'
                os.remove(Eliminar_zip)
                return render(self.request, self.template_name, {'msg_error': msg_error, 'form': form})

            ### Codigo de la aplicacion ###
            name_dir = os.path.dirname(metadata)
            codigo_app = name_dir

            ### Eliminar Extraccion ###
            Eliminar = path+'/'+name_dir
           
            #### Json Metadatos ####
            md = parsearFile(metadata)

            ### Ruta zip ###
            absoluta = os.path.abspath(FilePath)

            if md:
                ####  VALIDATORS IF EXISTS COD IN DB ####
                try:
                    models = metadata_model
                    validator = models.objects.get(codigo_app = codigo_app)
                    if validator.codigo_app == codigo_app:
                        message = ('Desea reemplazar la aplicacion registrada ('+validator.nombre+') por la que se esta cargando ('+validator.nombre+')')

                    ide = md[2]
                    for ky, vl in ide.iteritems():
                        ide_app = vl

                    version = md[3]
                    for key, val in version.iteritems():
                        version_app = val

                    version_key = version.keys()
                    version_value = version.values()
                         
                    nombre = md[0]
                    for clave, valor in nombre.iteritems():
                        nombre_app = valor

                    nombre_key = nombre.keys()
                    nombre_value = nombre.values()

                    shutil.rmtree(Eliminar)

                    '''
                    Rutina que hace el envio del archivo a la capa de enlace para Actualziar [Update(crUd)]
                    Autor: Luis Guillermo Echenique lechenique@cenditel.gob.ve
                    Fecha: 22-05-2017
                    '''
                    url = settings.URL_API_REST+'archivo/'+ide_app+'/'
                    files = {'doc': open(absoluta, 'rb')}

                    r = requests.put(url,data = {'archivo_nombre': nombre_app, 'id_app':ide_app, 'version':version_app, 'codigo_app': codigo_app}, files=files)
                    if r.status_code==200:
                        os.remove(absoluta)

                    print "----- Envio del archivo a la capa de enlace para actualizar!!! -----"
                    return render(self.request, self.template_name, {'form': form , 'metadatos': json.dumps(md) , 'codigo_app': codigo_app ,'version_app': version_app, 'nombre_app': nombre_app, 'id': ide_app, 'MSG': message , 'absoluta': absoluta })

                except models.DoesNotExist:
                    ide = md[2]
                    for ky, vl in ide.iteritems():
                        ide_app = vl

                    version = md[3]
                    for key, val in version.iteritems():
                        version_app = val

                    version_key = version.keys()
                    version_value = version.values()
                         
                    nombre = md[0]
                    for clave, valor in nombre.iteritems():
                        nombre_app = valor

                    nombre_key = nombre.keys()
                    nombre_value = nombre.values()
                    message = ('Desea realizar el registro de la aplicacion ('+nombre_app+')')

                    shutil.rmtree(Eliminar)
                    
                    '''
                    Rutina que hace el envio del archivo a la capa de enlace 
                    Autor: Luis Guillermo Echenique lechenique@cenditel.gob.ve
                    Fecha: 22-05-2017
                    '''
                    url = settings.URL_API_REST+'archivo/'
                    files = {'doc': open(absoluta, 'rb')}

                    r = requests.post(url,data = {'archivo_nombre': nombre_app, 'id_app':ide_app, 'version':version_app, 'codigo_app': codigo_app}, files=files)
                    if r.status_code==201:
                        os.remove(absoluta)
                    print "----- Envio del archivo a la capa de enlace!!! -----"
                    return render(self.request, self.template_name, {'form': form , 'metadatos': json.dumps(md) , 'codigo_app': codigo_app ,'version_app': version_app, 'nombre_app': nombre_app, 'id': ide_app, 'MSG': message ,  })
            else:
                form = registrar_form
                msg_error = 'El archivo No cumple con los requeisitos'
                return render(self.request, self.template_name, {'msg_error': msg_error, 'form': form})

        except zipfile.BadZipfile, err:
            form = registrar_form
            msg_error = 'El archivo no es un .zip'
            return render(self.request, self.template_name, {'msg_error': msg_error, 'form': form})  


def metadatos_get_data(request):
    nombre = request.GET.get('nombre', None)
    id_organizacion = request.GET.get('id_organizacion', None)
    id = request.GET.get('id', None)
    codigo_app = request.GET.get('codigo_app', None)
    version = request.GET.get('version', None)
    clase_inicial = request.GET.get('clase_inicial', None)
    
    ### aqui llaga la respuesta de la API del envio del file y de la verificacion de existencia ###
    checked_app = requests.get(settings.URL_API_REST+'api_rest/checked_exists/'+codigo_app+'?format=json')
    respuesta = checked_app.content

    try:
        ### Consulta a la base de datos la aplicacion que sera reemplazada ###
        model = metadata_model
        val = model.objects.get(id_app = id)

        ### valida que todo exista ###
        if val.id_app == id and nombre and id_organizacion and id and codigo_app and version and clase_inicial:
            ### Update app si existe ###
            update_app = model.objects.get(id_app = id)
            update_app.nombre = nombre
            update_app.id_organizacion = id_organizacion
            update_app.codigo_app = codigo_app
            update_app.version = version
            update_app.clase_inicial = clase_inicial
            update_app.save()

            ### Eliminar directorio despues de culminar ###
            '''
            modelo_ruta = registrar_app
            obj = modelo_ruta.objects.latest("pk")
            ruta = obj.cargar_app
            FilePath = str(ruta)
            absoluta = os.path.abspath(FilePath)
            os.remove(absoluta)
            '''

            ### Mensaje de exito ###
            print "----- La aplicacion "+nombre+" fue reemplazada -----"
            message_er = ('La aplicacion ('+nombre+') fue reemplazada')
            
            return JsonResponse(message_er,safe=False)

    except model.DoesNotExist:
        if nombre and id_organizacion and id and codigo_app and version and clase_inicial:
            ### Almacenar app de no existir ###
            modelo = metadata_model()
            modelo.nombre = nombre
            modelo.id_organizacion = id_organizacion
            modelo.id_app = id
            modelo.codigo_app = codigo_app
            modelo.version = version
            modelo.clase_inicial = clase_inicial
            ### Falta validar modelo ###
            modelo.save()

            ### Eliminar directorio despues de culminar ###
            '''
            modelo_ruta = registrar_app
            obj = modelo_ruta.objects.latest("pk")
            ruta = obj.cargar_app
            FilePath = str(ruta)
            absoluta = os.path.abspath(FilePath)
            os.remove(absoluta)
            '''

            message_ex = 'La aplicacion ('+nombre+') se registro de manera correcta'
            return JsonResponse(message_ex,safe=False)


def listar_app_view(request):
    return render_to_response('listar.template.html', {}, context_instance=RequestContext(request))


class ListDataJsonView(BaseDatatableView):
    model = metadata_model
    columns = ['nombre', 'codigo_app' , 'id_app', 'version']
    order_columns = ['id_app', 'codigo_app' , 'nombre', 'version']
    max_display_length = 500

    def __init__(self):
        super(ListDataJsonView, self).__init__()

    def get_initial_queryset(self):
        return self.model.objects.all()

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
            item.id_app,
            item.codigo_app,
            item.nombre,
            item.version
            ])
        return json_data


def zip_get_data(request):
    zipfile = request.POST.post('form', None)
    return JsonResponse(zipfile,safe=False)


def delete_get_data(request):
    id = request.GET.get('id', None)
    codigo = request.GET.get('codigo', None)
    nombre = request.GET.get('nombre', None)
    checked_app = requests.get(settings.URL_API_REST+'api_rest/checked_exists/'+codigo+'?format=json')
    respuesta = checked_app.content
    string = str(respuesta)
    if string == 'true':
        checked_edo_app = requests.get(settings.URL_API_REST+'api_rest/checked_edo_app/'+codigo+'?format=json')
        result = checked_edo_app.content
        decode_data = json.loads(result)
        opciones = ()
        for x in range(len(decode_data)):
            j = decode_data[x]
            servicio = j['servicio']
            estado =  j['Estado']
            message = 'La aplicacion '+nombre+' esta en estado '+estado+' por el servicio '+servicio
        return JsonResponse(message,safe=False)
    else:
        if string == 'false':
            message = 'La aplicacion '+nombre+' no existe'
            return JsonResponse(message,safe=False)


def delete_get_data(request):
    codigo = request.GET.get('codigo', None)
    model = metadata_model
    ap = model.objects.get(codigo_app = codigo)
    ap.delete()
    eliminar = requests.get(settings.URL_API_REST+'api_rest/eliminar/'+codigo+'?format=json')
    eliminado = eliminar.content
    loads_data = json.loads(eliminado)

    return JsonResponse(loads_data,safe=False)
