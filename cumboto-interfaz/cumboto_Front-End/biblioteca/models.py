# -*- coding: utf-8 -*-
from django.db import models
from django.core.files.base import File
from biblioteca.validators import valid_extension
import os
from sys import argv
from zipfile import BadZipfile, ZipFile
import urllib2, sys, zipfile
from shutil import * 


def generate_path(instance, filename):
    folder = os.path.join("tmp", filename)
    return folder


class registrar_app(models.Model):
    cargar_app = models.FileField(
        blank=True, null=True, upload_to=generate_path,
        validators=[valid_extension])

    def __unicode__(self):
        return self.cargar_app


class metadata_model(models.Model):
    nombre = models.CharField(max_length=25,)
    id_organizacion = models.CharField(max_length=25,)
    id_app = models.CharField(max_length=25, primary_key=True)
    codigo_app = models.CharField(max_length=25,)
    version = models.CharField(max_length=25,)
    clase_inicial = models.CharField(max_length=25,)