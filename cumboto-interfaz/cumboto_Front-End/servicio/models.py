# -*- coding: utf-8 -*-
"""
Sistema para transmisión de aplicaciones desde las salas de control maestro de TV (CUMBOTO)
Copyleft (@) 2017 CENDITEL nodo Mérida - https://cumaco.cenditel.gob.ve/desarrollo/wiki/ftransporte
"""
## @namespace capa.models
#
# Contiene las clases, atributos, métodos y/o funciones a implementar para los modelos del módulo de servicios
# @author Jhonathan Salas Segura (jsalas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>

from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Clases Consulta de Servicios
class servicioModel(models.Model):
    servicio = models.CharField(help_text=("Servicios disponibles"), max_length=100, primary_key=True)    
    ranura = models.IntegerField(help_text=("Numero de ranura"))
    cod_servicio = models.CharField(help_text=("Codigo del servicio"), max_length=100, null=True)
    nom_servicio = models.CharField(help_text=("Nombre del servicio"), max_length=100, null=True)
    cod_api = models.CharField(help_text=("Codigo de la aplicacion"), max_length=100)
    nom_api = models.CharField(help_text=("Nombre de la aplicacion"), max_length=100)
    modalidad = models.CharField(help_text=("Modalidad en que se encuentra la aplicacion"), max_length=15, null=True)

# Clases Configurar Servicio Emergente
class DataModel(models.Model):
    ranura = models.IntegerField(help_text=("Numero de ranura"))
    codigo_app = models.CharField(help_text=("Codigo de la aplicacion"), max_length=100)
    modalidad = models.CharField(help_text=("Modalidad en que se encuentra la aplicacion"), max_length=15, null=True)
