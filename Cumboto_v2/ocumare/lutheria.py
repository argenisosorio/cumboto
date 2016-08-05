# -*- coding: utf-8 -*-
#*
#* cumaco ocumare - Gestión de la transmisión de flujos multimedia para TDA
#*
#* Derecho de autor (C) 2015-2016 Dhionel Díaz, Laura Colina. Fundación
#* 	Centro Nacional de Desarrollo e Investigación en Tecnologías (CENDITEL).
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
#* Este archivo es parte de cumaco ocumare.
#*
#* lutheria.py	- Biblioteca para construcción de tablas PSI y carrusel de datos
#*		  en el sistema de transmisión de TDA Cumaco.
#*
#* El desarrollo del código en el presente archivo tuvo como referencia algunos
#* elementos originalmente publicados en el documento "OpenCaster para SATVD-T"
#* elaborado por el Laboratorio  de Investigación  y Formación  en  Informática
#* Avanzada (LIFIA). Facultad de Informática. Universidad Nacional de La Plata.
#* República Argentina. Mayo de 2011.

import os
import sys
import shutil
import subprocess
import ConfigParser
import psi
import filelock
import re
from functools import wraps

class tsco(object):
	APP_CONTROL_AUTO = 0x01
	def __init__(self, ruta_conf, nv_edo = None):
		cf = ConfigParser.SafeConfigParser()
		cf.read(ruta_conf)
		ruta_trans = cf.get('Transmision', 'ruta')

		self.conf = cf
		self.ruta_trans = ruta_trans

		# Cerrojo global de la instancia
		self.cerrojo = filelock.FileLock(os.path.join(ruta_trans, 'cerrojo'))

		# Estado de las aplicaciones
		self.app_edo_reg = ConfigParser.SafeConfigParser()
		self.app_edo_reg.read(os.path.join(ruta_trans, 'estado_app.conf'))
		aer = self.app_edo_reg

		# Estado de los servicios
		self.serv_edo_reg = ConfigParser.SafeConfigParser()
		self.serv_edo_reg.read(os.path.join(ruta_trans, 'estado_serv.conf'))
		ser = self.serv_edo_reg

		# Estado de la red
		self.red_edo_reg = ConfigParser.SafeConfigParser()
		self.red_edo_reg.read(os.path.join(ruta_trans, 'estado_red.conf'))

		######################################################################
		self.app_biblio = cf.get('Aplicaciones', 'biblioteca')

		self.red = {
			'network_name':		cf.get('Red', 'nombre'),
			'area_code':		int(cf.get('Red', 'codigo_area'), 0),
			'guard_interval':	int(cf.get('Red', 'intervalo_guarda'), 0),
			'transmission_mode':	int(cf.get('Red', 'modo_transmision'), 0),
			'ts_id':		int(cf.get('Red', 'id'), 0),
			'orig_network_id':	int(cf.get('Red', 'id_orig'), 0),
			'ts_freq':		int(cf.get('Red', 'frecuencia'), 0),
			'ts_remote_control_key':int(cf.get('Red', 'tecla_control_remoto'), 0),
		}
		# Obteniendo numero de servicios configurados
		ns = int(cf.get('Red', 'num_servicios'), 0)
		self.ns = ns

		self.svc_md = []
		self.service_id = []
		self.pmt_pid = []
		self.ait_pid = []
		self.pmt_par = []
		self.app_edo = [None] * ns
		self.app_md  = [None] * ns
		self.ait_v = []
		self.pmt_v = []
		nv_carrusel = False

		for i in range(ns):
			self.svc_md.append(
				{
					'np': cf.get('servicio_%s' % i, 'proveedor'),
					'n': cf.get('servicio_%s' % i, 'nombre'),
				}
			)
			# ID de servicio de TV Digital. (16 bit):
			# ABNT NBR 15603-2:2007 - Anexo H - sección H.3 Service_id
			# network_id(10-0)-service type-service number
			# ts_id(10-0) - 00 - sn
			self.service_id.append(int(cf.get('servicio_%s' % i, 'id'), 0))
			# PID de la PMT del servicio.
			self.pmt_pid.append(int(cf.get('servicio_%s' % i, 'pmt_pid'), 0)) 
			# ID de tabla AIT
			self.ait_pid.append(int(cf.get('servicio_%s' % i, 'ait_pid'), 0))
			self.pmt_par.append(
				{
					'pid_video': int(cf.get('servicio_%s' % i, 'video_pid'), 0),
					'pid_audio': int(cf.get('servicio_%s' % i, 'audio_pid'), 0),
					'app_par': None,
				}
			)
			# Versión de tabla PSI/SI
			self.ait_v.append(int(ser.get('servicio_%s' % i, 'ait_v'), 0))
			self.pmt_v.append(int(ser.get('servicio_%s' % i, 'pmt_v'), 0))
			# Datos y estado de las aplicaciones
			na = int(cf.get('servicio_%s' % i, 'num_app'), 0)
			if na > 0:
				self.pmt_par[i]['app_par'] = []
				self.app_edo[i] = []
				self.app_md[i] = []
			for j in range(na):
				self.pmt_par[i]['app_par'].append(
					{
						'pid_carrusel': int(cf.get('app_%s_%s' % (i, j), 'pid_carrusel'), 0),
						'id_carrusel' : int(cf.get('app_%s_%s' % (i, j), 'id_carrusel'), 0),
						'component_tag' : int(cf.get('app_%s_%s' % (i, j), 'etiqueta_asoc'), 0),
					}
				)
				self.app_edo[i].append(
					{
						'codigo': aer.get('app_%s_%s' % (i, j), 'codigo'),
						'control': int(aer.get('app_%s_%s' % (i, j), 'control'), 0),
						'version': int(aer.get('app_%s_%s' % (i, j), 'version'), 0),
					}
				)
				if nv_edo and nv_edo['serv'] == i and nv_edo['app'] == j:
					nv_edo, nv_carrusel = self.nv_edoc(nv_edo = nv_edo, act_md = False)
				md = ConfigParser.SafeConfigParser()
				md.read(os.path.join(self.app_biblio,
					self.app_edo[i][j]['codigo'], 'metadatos.conf')
				)
				self.app_md[i].append(
					{
						'organisation_id': int(md.get('metadatos', 'id_organizacion'), 0),
						'id': int(md.get('metadatos', 'id'), 0),
						'version': md.get('metadatos', 'version'),
						'control_code': self.app_edo[i][j]['control'],
						'name': md.get('metadatos', 'nombre'),
						'initial_class': md.get('metadatos', 'clase_inicial'),
					}
				)

		# Versión de tabla PSI/SI
		self.nit_v = int(self.red_edo_reg.get('Red', 'nit_v'), 0);
		self.sdt_v = int(self.red_edo_reg.get('Red', 'sdt_v'), 0);
		self.pat_v = int(self.red_edo_reg.get('Red', 'pat_v'), 0);

		# Aplicación para relleno
		self.app_rell = self.red_edo_reg.get('Red', 'app_rell')

		self.pr_edoc(nv_edo, nv_carrusel)

	######################################################################
	def _serializar(f):
		@wraps(f)
		def r_f(self, *args, **kwargs):
			with self.cerrojo:
				return f(self, *args, **kwargs)
		return r_f

	######################################################################
	def nv_edoc(self, nv_edo, act_md = True):
		s = nv_edo['serv']
		a = nv_edo['app']
		nv_carrusel = False

		if (s < len(self.app_edo) and self.app_edo[s] and a < len(self.app_edo[s]) and (
				self.app_edo[s][a]['codigo'] != nv_edo['cod'] or
				self.app_edo[s][a]['control'] != nv_edo['ctl']
			) and (
				self.app_edo[s][a]['control'] == nv_edo['ctl'] or
				nv_edo['ctl'] != self.APP_CONTROL_AUTO or
				sum(1 for ap in self.app_edo[s] if ap['control'] == self.APP_CONTROL_AUTO) < 1
			)
		):
			if self.app_edo[s][a]['codigo'] != nv_edo['cod']:
				self.app_edo[s][a]['codigo']   = nv_edo['cod']
				self.app_edo[s][a]['version'] += 1
				self.app_edo[s][a]['version'] %= 0x10
				self.app_edo_reg.set(
					'app_%s_%s' % (s, a), 'codigo',
					self.app_edo[s][a]['codigo']
				)
				self.app_edo_reg.set(
					'app_%s_%s' % (s, a), 'version',
					hex(self.app_edo[s][a]['version'])
				)
				if act_md: 
					md = ConfigParser.SafeConfigParser()
					md.read(os.path.join(
						self.app_biblio,
						self.app_edo[s][a]['codigo'],
						'metadatos.conf'
					))
					self.app_md[s][a]['organisation_id']	= int(
						md.get('metadatos', 'id_organizacion'), 0
					)
					self.app_md[s][a]['id']		= int(
						md.get('metadatos', 'id'), 0
					)
					self.app_md[s][a]['version']		= md.get('metadatos', 'version')
					self.app_md[s][a]['control_code']	= self.app_edo[s][a]['control']
					self.app_md[s][a]['name']		= md.get('metadatos', 'nombre')
					self.app_md[s][a]['initial_class']	= md.get('metadatos', 'clase_inicial')
				nv_carrusel = True
			self.app_edo[s][a]['control'] = nv_edo['ctl']
			self.app_edo_reg.set(
				'app_%s_%s' % (s, a), 'control', str(self.app_edo[s][a]['control'])
			)
			self.ait_v[s] += 1
			self.ait_v[s] %= 0x20
			self.pmt_v[s] += 1 
			self.pmt_v[s] %= 0x20 
			self.serv_edo_reg.set('servicio_%s' % s, 'ait_v', hex(self.ait_v[s]))
			self.serv_edo_reg.set('servicio_%s' % s, 'pmt_v', hex(self.pmt_v[s]))
		else:
			nv_edo = None
		return nv_edo, nv_carrusel

	######################################################################
	def pr_edoc(self, nv_edo, nv_carrusel):
		if nv_edo:
			with open(os.path.join(self.ruta_trans, 'estado_app.conf'), 'w') as f_a, \
				open(os.path.join(self.ruta_trans, 'estado_serv.conf'), 'w') as f_s:
				self.app_edo_reg.write(f_a)
				self.serv_edo_reg.write(f_s)
			self.gen_tablas({'pat': False, 'sdt': False, 'nit': False,
				'ait': [j == nv_edo['serv'] for j in range(len(self.app_md))],
				'pmt': [j == nv_edo['serv'] for j in range(len(self.pmt_par))]
			})
			if nv_carrusel:
				self.gen_carrusel(nv_edo['serv'], nv_edo['app'])

	######################################################################
	@_serializar
	def gen_tablas(self, sel = None):
		tablas = []
		# TABLA NIT
		if not sel or 'nit' not in sel or sel['nit']:
			tablas.append({
				'ruta': os.path.join(self.ruta_trans, 'nit.ts'),
				'pid': psi.nit_pid,
				'dat': psi.ni_section(
					self.nit_v,
					self.service_id,
					self.red['orig_network_id'],
					self.red['ts_id'],
					self.red['network_name'],
					self.red['area_code'],
					self.red['guard_interval'],
					self.red['transmission_mode'],
					self.red['ts_freq'],
					self.red['ts_remote_control_key']
				)
			})
		# TABLA SDT
		if not sel or 'sdt' not in sel or sel['sdt']:
			tablas.append({
				'ruta': os.path.join(self.ruta_trans, 'sdt.ts'),
				'pid': psi.sdt_pid,
				'dat': psi.sd_section(
					self.sdt_v, self.service_id, self.svc_md,
					self.red['ts_id'],
					self.red['orig_network_id']
				)
			})
		# TABLA PAT
		if not sel or 'pat' not in sel or sel['pat']:
			tablas.append({
				'ruta': os.path.join(self.ruta_trans, 'pat.ts'),
				'pid': 0,
				'dat': psi.pa_section(
					self.pat_v, self.service_id,
					self.pmt_pid, self.red['ts_id']
				)
			})
		# TABLAS AIT
		# ait = [None] * len(self.app_md)
		for i in range(len(self.app_md)):
			if (not sel or 'ait' not in sel or sel['ait'][i]) and self.app_md[i]:
				tablas.append({
					'ruta': os.path.join(self.ruta_trans, 'ait_%s.ts' % i),
					'pid': self.ait_pid[i],
					'dat': psi.ai_section(
						self.ait_v[i], self.pmt_par[i]['app_par'],
						self.app_md[i]
					)
				})
		# TABLAS PMT
		# pmt = [None] * len(self.pmt_par)
		for i in range(len(self.pmt_par)):
			if not sel or 'pmt' not in sel or sel['pmt'][i]:
				tablas.append({
					'ruta': os.path.join(self.ruta_trans, 'pmt_%s.ts' % i),
					'pid': self.pmt_pid[i],
					'dat': psi.pm_section(
						self.pmt_v[i], self.service_id[i], self.pmt_par[i],
						self.ait_pid[i], self.ait_v[i], self.app_md[i]
					)
				})
		######################################################################
		# Creación de archivos de salida
		a_s = open(os.devnull, 'w')
		for tb in tablas:
			with open(tb['ruta'] + '.n', 'wb') as f:
				proc = subprocess.Popen(['sec2ts', str(tb['pid'])],
					stdin = subprocess.PIPE, stdout = f, stderr = a_s,
					close_fds = True)
				proc.communicate(tb['dat'].pack())
			os.rename(tb['ruta'] + '.n', tb['ruta'])

	######################################################################
	@_serializar
	def gen_carrusel(self, s, a):
		if not (s < len(self.app_edo) and self.app_edo[s] and a < len(self.app_edo[s])):
			return
		if os.access(os.path.join(self.ruta_trans, 'aplicacion'), os.F_OK):
			shutil.rmtree(os.path.join(self.ruta_trans, 'aplicacion'))
		shutil.copytree(
			os.path.join(self.app_biblio, self.app_edo[s][a]['codigo'], 'aplicacion'),
			os.path.join(self.ruta_trans, 'aplicacion')
		)
		compress_mode = '0'
		padding_on = '1'
		clean_off = '0'
		ddb_size = '4066'
		update_flag = '0'
		mount_frequency = '3'
		a_e = open(os.devnull, 'r')
		a_s = open(os.devnull, 'w')
		proc = subprocess.Popen(
			[
				'oc-update', 'aplicacion', hex(self.pmt_par[s]['app_par'][a]['component_tag']),
				hex(self.app_edo[s][a]['version']),
				str(self.pmt_par[s]['app_par'][a]['pid_carrusel']),
				str(self.pmt_par[s]['app_par'][a]['id_carrusel']),
				compress_mode, padding_on, clean_off, ddb_size,
				update_flag, mount_frequency
			],
			stdin = a_e, stdout = a_s, stderr = a_s,
			close_fds = True, cwd = self.ruta_trans
		)
		proc.wait()
		shutil.rmtree(os.path.join(self.ruta_trans, 'aplicacion'))
		os.rename(
			os.path.join(self.ruta_trans, 'aplicacion.ts'),
			os.path.join(self.ruta_trans, 'app_%s_%s.ts' % (s, a))
		)

	######################################################################
	@_serializar
	def gen_nv_carrusel(self, s, a):
		if (s < len(self.app_edo) and self.app_edo[s] and a < len(self.app_edo[s])):
			self.app_edo[s][a]['version'] += 1
			self.app_edo[s][a]['version'] %= 0x10
			self.app_edo_reg.set(
				'app_%s_%s' % (s, a), 'version',
				hex(self.app_edo[s][a]['version'])
			)
			self.gen_carrusel(s, a)
			with open(os.path.join(self.ruta_trans, 'estado_app.conf'), 'w') as f_a:
				self.app_edo_reg.write(f_a)
	

	######################################################################
	# Método act_carrusel_app(self, app_cod)
	#
	#	Genera un nuevo carrusel para las ranuras que estén usando la
	#	aplicación cuyo código en la biblioteca es app_cod. La versión
	#	de cada nuevo carrusel es incrementada en 1 mod 0x10.
	#
	# Argumentos:
	#	app_cod -> Código de aplicación en la biblioteca con el cual
	#		   realizar la operación.
	#
	@_serializar
	def act_carrusel_app(self, app_cod):
		for s in range(len(self.svc_md)):
			if self.app_edo[s]:
				for a in range(len(self.app_edo[s])):
					if self.app_edo[s][a]['codigo'] == app_cod :
						self.gen_nv_carrusel(s, a)

	######################################################################
	@_serializar
	def gen_nvtsco(self, nv_edo):
		try:
			if not nv_edo:
				return False
			nv_edo, nv_carrusel = self.nv_edoc(nv_edo = nv_edo)
			self.pr_edoc(nv_edo, nv_carrusel)
		except:
			return False
		return True

	######################################################################
	@_serializar
	def detener_ranura(self, s, a):
		if s in range(len(self.svc_md)) and a in range(len(self.app_edo[s])):
			self.gen_nvtsco({
				'serv': s,
				'app': a,
				'cod': self.app_rell,
				'ctl': 2
			})

	######################################################################
	@_serializar
	def retirar_app(self, app_cod):
		if app_cod == self.app_rell:
			return
		for s in range(len(self.svc_md)):
			if self.app_edo[s]:
				for a in range(len(self.app_edo[s])):
					if self.app_edo[s][a]['codigo'] == app_cod :
						self.detener_ranura(s, a)

	######################################################################
	@_serializar
	def bib_borrar_app(self, app_cod):
		if app_cod == self.app_rell or not re.match('[0-9A-Fa-f]{12}', app_cod):
			return
		shutil.rmtree(os.path.join(self.app_biblio, app_cod))

	######################################################################
	@_serializar
	def bib_copiar_app(self, app_ruta):
		app_cod = os.path.basename(app_ruta)
		if not (
			os.path.isdir(app_ruta) and
			re.match('[0-9A-Fa-f]{12}', app_cod) and
			os.path.isfile(os.path.join(app_ruta, 'metadatos.conf')) and
			os.path.isdir(os.path.join(app_ruta, 'aplicacion'))
		):
			return False
		shutil.copytree(app_ruta, os.path.join(self.app_biblio, app_cod))
		return True

	######################################################################
	@_serializar
	def eliminar_app(self, app_cod):
		self.retirar_app(app_cod)
		self.bib_borrar_app(app_cod)
	
	######################################################################
	@_serializar
	def obt_app_rell_global(self):
		return self.app_rell

	######################################################################
	# Método obt_serv_md(self)
	#
	#	Proporciona lista con metadatos de cada servicio
	#
	# Retorna:
	#	Lista de diccionarios cuyos componentes son:
	#		np -> nombre del proveedor
	#		n  -> nombre del servicio
	#
	@_serializar
	def obt_serv_md(self):
		return self.svc_md

	######################################################################
	# Método obt_edo_ranuras(self, s)
	#
	#	Proporciona lista con datos de estado de las ranuras de un servicio.
	#
	# Argumentos:
	#	s -> número del servicio cuyos datos se requieren.
	#
	# Retorna:
	#	Lista de diccionarios cuyos componentes son:
	#		codigo  -> código de identificación de la aplicación en la biblioteca.
	#		control -> código de control de ejecución (automática, en menú, etc.)
	#
	#	Si el número de servicio fuera inválido o el servicio no tuviese ranuras activadas
	#	se retorna None
	#
	@_serializar
	def obt_edo_ranuras(self, s):
		if s in range(len(self.app_edo)) and self.app_edo[s]:
			app_edo_s = []
			for a in range(len(self.app_edo[s])):
				app_edo_s.append(
					{
						'codigo': self.app_edo[s][a]['codigo'],
						'control': self.app_edo[s][a]['control'],
					}
				)
			return app_edo_s
		else:
			return None

    #######################################################################
	@_serializar
	def check_app(self,codigo_apps):
		# Verificación del codigo de la aplicación según el patrón
		if re.match('[0-9A-Fa-f]{12}', codigo_apps):
			if os.path.isdir(os.path.join(self.app_biblio, codigo_apps)):
				return True
			else:
				return False
		else:
			return 'El codigo de la aplicacion no cumple con el patron'

    #####################################################################
	@_serializar
	def check_edo(self,codigo_apps):
		if re.match('[0-9A-Fa-f]{12}', codigo_apps):
			app_edos = []
			app_edo_codigo = [None] * self.ns
			for i in range(self.ns):
				# Datos y estado de las aplicaciones
				na = int(self.conf.get('servicio_%s' % i, 'num_app'), 0)
				if na > 0:
					app_edo_codigo[i] = []
					for j in range(na):
						# Aplicaciones que se encuentran asignadas en los
						#  servicios que se estan transmitiendo
						app_edo_codigo[i].append(
							self.app_edo_reg.get('app_%s_%s' % (i, j), 'codigo'),
						)
						if codigo_apps in app_edo_codigo[i]:
							app_edos.append(
								{
									'Estado': 'Ocupada',
									'servicio': self.conf.get('servicio_%s' % i, 'nombre'),
									'control': int(self.app_edo_reg.get('app_%s_%s' % (i, j), 'control'), 0),
									'codigo': self.app_edo_reg.get('app_%s_%s' % (i, j), 'codigo'),
								}
							)
							return app_edos
		else:
			return 'El codigo de la aplicacion no cumple con el patron'
