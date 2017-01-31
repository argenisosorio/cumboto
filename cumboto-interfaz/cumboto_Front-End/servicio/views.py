# Create your views here.
# -*- coding: utf-8 -*-
    ###################################################################################################
    #   ######## #####      ###              ###   #####  ##       #  #####  ###### ###### ########   #
    #      ##    ##   ##  ##   ##          ##   ## ##   # ##      #   ##   # ##     ##        ##      #
    #      ##    ##    ## #######  ######  ####### #####  ##     #    #####  ####   ######    ##      #
    #      ##    ##    ## ##   ##          ##   ## ##     ##    #     ##  ## ##         ##    ##      #
    #      ##    #####    ##   ##          ##   ## ##     ##   #      ##  ## ###### ######    ##      #
    ###################################################################################################

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
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from .models import servicioModel
from biblioteca.models import metadata_model
from .forms import servicioForm
import json
import requests
from django.conf import settings
from django.views.generic import CreateView, TemplateView
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .models import servicioModel
from .forms import servicioForm, SelectForm
from django.shortcuts import render_to_response
from django.template import loader, Context,  RequestContext
from django_datatables_view.base_datatable_view import BaseDatatableView

###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################

class servicioView(CreateView):

    """!
    Clase que permite almacenar los datos solicitados al servidor
    @author Hugo Ramirez (hramirez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 08-06-2016
    """

    model = servicioModel
    form_class = servicioForm
    template_name = 'base.servicio.html'
    success_url = reverse_lazy('global')

    def form_valid(self, form):


        self.object = form.save(commit=False)
        self.object.servicio = form.cleaned_data['servicio']
        self.object.ranura = form.cleaned_data['ranura']
        self.object.codigo_app = form.cleaned_data['codigo_app']
        self.object.modalidad = form.cleaned_data['modalidad']
        self.object.save()

        return super(servicioView, self).form_valid(form)


###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################

def GLOBAL_REST_FRAMEWORK(request):
    form = servicioForm()
    return render_to_response('base.servicio.html', {'form': form}, context_instance=RequestContext(request))

def configurar_omision(request):
    form = servicioForm()
    return render(request, 'base.omision.servicio.html', {'form': form})

def CONSULT_REST(request):
    form = SelectForm()
    return render(request, 'base.consulta.servicio.html', {'form': form})

###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
def servicios_get_data(request):

    api = requests.get(settings.URL_API_REST+'api_rest/listar?format=json')
    servicios = api.content
    decode_data = json.loads(servicios)
    opciones = ()
    for x in range(len(decode_data)):
        j = decode_data[x]
        opciones += (j['codigo'], j['n']),
        
    return JsonResponse(decode_data,safe=False)

###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
def ranuras_get_data(request):

    serv = request.GET.get('servicio', None)
    ranura_data = requests.get(settings.URL_API_REST+'api_rest/ranuras/'+serv+'?format=json')
    ranuras = ranura_data.content
    decode_data = json.loads(ranuras)

    if len(decode_data) == 2:
        ranuras = 2
        ranura0 = decode_data[0]

        ### Ranura (0) ###
        control_0 = ranura0['control']
        codigo_0 = ranura0['codigo']
        #model = metadata_model
        #Aplicacion = model.objects.get(codigo_app = codigo_0)
        #nombre_0 = Aplicacion.nombre


        ranura_text0 = "Ranura 0"
        ranura_0 = 0

        if control_0 == 1:
            ctl = "Automatico"
        else:
            if control_0 == 2:
                ctl = "Menu"

         ### Ranura (1) ###
        ranura1 = decode_data[1]
        control_1 = ranura1['control']
        codigo_1 = ranura1['codigo']
        #model = metadata_model
        #Aplicacion = model.objects.get(codigo_app = codigo_1)
        #nombre_1 = Aplicacion.nombre


        ranura_text1 = "Ranura 1"
        ranura_1 = 1

        if control_1 == 1:
            ctl1 = "Automatico"
        else:
            if control_1 == 2:
                ctl1 = "Menu"

        ### Data For Data Table ###
        lista = [[ranura_0, codigo_0, ctl, serv],[ranura_1, codigo_1, ctl1, serv]]
        return JsonResponse(lista,safe=False)
    else:
        if len(decode_data) == 1:
            
            ### Ranura (0) ###
            control_0 = ranura0['control']
            codigo_0 = ranura0['codigo']
         
            ranura_text0 = "Ranura 0"
            ranura_0 = 0

            if control_0 == 1:
                ctl = "Automatico"
            else:
                if control_0 == 2:
                    ctl = "Menu"
            lista = [[ranura_0, codigo_0, ctl, serv]]
            return JsonResponse(lista,safe=False)
        else:
            if decode_data == 'Servicio Inactivo':
                return JsonResponse(False,safe=False)


###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
class TableDataJsonView(BaseDatatableView):
   
    model = servicioModel
  
    columns = ['ranura_str', 'nombre' , 'modalidad_str']
    
    order_columns = ['ranura_str', 'nombre' , 'modalidad_str']
   
    max_display_length = 500

    def __init__(self):
        super(TableDataJsonView, self).__init__()

    def get_initial_queryset(self):
       
        return self.model.objects.all()

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
            item.ranura_str,
            item.nombre,
            item.modalidad_str
            ])
        return json_data

###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
def correr_get_data(request):

    serv = request.GET.get('serv', None)
    app = request.GET.get('app', None)
    cod = request.GET.get('cod', None)
    ctl = request.GET.get('ctl', None)
    if serv and app and cod and ctl:
        new_status = requests.get(settings.URL_API_REST+'api_rest/nv_edo/'+serv+'/'+app+'/'+cod+'/'+ctl+'?format=json')
        new = new_status.content
        if str(new) == 'true':
            message = 'Configuracion exitosa'
            return JsonResponse(message,safe=False)
        else:
            message = 'Ocurrio un error en la configuracion'
            return JsonResponse(message,safe=False)

    else:
        message = 'Selecione todos los elementos'
        return JsonResponse(message,safe=False)

###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
def aplicaciones_get_data(request):

    listar_aplicaciones = requests.get(settings.URL_API_REST+'api_rest/listar-aplicaciones?format=json')
    lista = listar_aplicaciones.content
    loads_data = json.loads(lista)
    opciones = ()
    for x in range(len(loads_data)):
        j = loads_data[x]
        opciones += (j['nombre'], j['codigo']),

    return JsonResponse(opciones,safe=False)

###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
def detener_get_data(request):

    serv = request.GET.get('serv', None)
    app = request.GET.get('app', None)

    detener = requests.get(settings.URL_API_REST+'api_rest/detener/'+serv+'/'+app+'?format=json')
    detenido = detener.content
    loads_data = json.loads(detenido)

    return JsonResponse(loads_data,safe=False)


###################################################
#       CONFIGURACION DE SERVICIOS CUMBOTO        #
###################################################
def omision_get_data(request):

    cod = request.GET.get('cod', None)

    configurar_omision = requests.get(settings.URL_API_REST+'api_rest/omision/'+cod+'?format=json')
    configurado = configurar_omision.content
    return JsonResponse(configurado,safe=False)