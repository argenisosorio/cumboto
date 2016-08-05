# -*- coding: utf-8 -*-
#*
#* cumaco ocumare - Gestión de la transmisión de flujos multimedia para TDA
#*
#* Derecho de autor (C) 2016 Laura Colina, Fundación CENDITEL.
#*
#* La Fundación CENDITEL concede permiso para usar, copiar, distribuir y/o modi-
#* ficar este programa,  reconociendo el derecho que la humanidad posee al libre
#* acceso al conocimiento, bajo los términos de la licencia de software GPL ver-
#* sión 2.0 de la Free Software Foundation.
#* Este programa se distribuye con la esperanza de que sea útil, pero sin ningu-
#* na garantía;  tampoco las implícitas  garantías de MERCANTILIDAD o ADECUACIÓN
#* A UN PROPÓSITO PARTICULAR.
#*
#* Para mayor información sobre los términos de la licencia consulte:
#* http://www.gnu.org/licenses/gpl-2.0.html.
#*
#* listar.py	- Despliegue de los datos de las aplcaciones contenidas en la bi-
#* blioteca.

import os
import re
import ConfigParser

class listar(object):
        def __init__(self, ruta_conf):
		cf = ConfigParser.SafeConfigParser()
                cf.read(ruta_conf)
		ruta_apps = cf.get('Aplicaciones', 'biblioteca')
		self.conf = cf 
		self.ruta_apps = ruta_apps 
		self.list_file_md = []
		self.list_codigo = []
		self.app_md = {} 
		
		for directorio in os.listdir(self.ruta_apps):
		        if os.path.isdir(os.path.join(self.ruta_apps, directorio)):
				# Verificación del nombre del dedirectorio con el patrón
				if re.match('[0-9A-Fa-f]{12}', directorio):
					self.list_codigo.append(directorio)
					dirs = os.walk(os.path.join(self.ruta_apps, directorio))
					self.dirs = dirs

					# Archivos metadatos.conf de las aplicaciones
					for subpath, subdir, fichero in self.dirs:
						for metadatos in fichero:
						       	(nombreFichero, extension) = os.path.splitext(metadatos)
					       		if(extension == ".conf"):
			        			    	self.list_file_md.append(nombreFichero+extension)

#		print ('Lista de archivos de metadatos', self.list_file_md)
#		print ('Lista de directorios de apps', self.list_codigo)

	def obtener_md(self):	
		for i in range(len(self.list_codigo)):
			outfilename = os.path.join(os.path.join(self.ruta_apps, self.list_codigo[i]), self.list_file_md[i])
			self.ruta_file_md = outfilename
			md = ConfigParser.SafeConfigParser()
			md.read(self.ruta_file_md)

			# Información de las aplicaciones del archivo metadatos.conf
			self.app_md['codigo_aplicacion', self.list_codigo[i]] = {
		              		'organisation_id': int(md.get('metadatos', 'id_organizacion'), 0),
					'id': int(md.get('metadatos', 'id'), 0),
					'version': md.get('metadatos', 'version'),
                		        'name': md.get('metadatos', 'nombre'),
                                	'initial_class': md.get('metadatos', 'clase_inicial'),
                               }

		return self.app_md
