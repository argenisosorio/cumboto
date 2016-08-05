# -*- coding: utf-8 -*-
#*
#* cumaco ocumare - Gestión de la transmisión de flujos multimedia para TDA
#*
#* Derecho de autor (C) 2015 Dhionel Díaz, Fundación CENDITEL.
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
#* ocumare/psi.py - Biblioteca para construcción de tablas PSI en el sistema de
#*		    transmisión de TDA Cumaco.
#*
#* El código en el presente archivo  se ha basado en el que fue publicado en el
#* documento  "OpenCaster para SATVD-T"  elaborado por el Laboratorio de Inves-
#* tigación y Formación en Informática Avanzada (LIFIA). Facultad de Informáti-
#* ca. Universidad Nacional de La Plata. República Argentina. Mayo de 2011.


from dvbobjects.PSI.PAT import *
from dvbobjects.PSI.NIT import *
from dvbobjects.PSI.SDT import *
from dvbobjects.PSI.PMT import *

from dvbobjects.MPEG.Descriptors import *
from dvbobjects.SBTVD.Descriptors import *

## ginga
from dvbobjects.MHP.AIT import *
from dvbobjects.MHP.Descriptors import *

GINGA_J_application_type   = 0x0001
GINGA_NCL_application_type = 0x0009


# ID de tablas NIT y SDT
nit_pid			= 0x0010
sdt_pid			= 0x0011

######################################################################
######################################################################
# See Annex H of EN300468
# Posted: Fri Nov 15, 2013 11:52 am in:
# http://www.avalpa.com/forum/viewtopic.php?f=11&t=33
# by:  aventuri
#
# Retrieved on July 2 2015
#
class AAC_descriptor(Descriptor):
    descriptor_tag = 0x7C

    def bytes(self):
        for property, value in vars(self).iteritems():
            if not property in ['additional_info', 'AAC_type','profile_and_level']:
                print "WARN: unrecognized attribute ", property, " in object ", self
        stream = pack( "!B", self.profile_and_level)
        if hasattr (self, 'AAC_type') | hasattr (self, 'additional_info'):
            if hasattr (self, 'AAC_type'):
                stream += pack("BB", 0xFF, self.AAC_type)
            else:
                stream += pack("B", 0x7F)
            if hasattr (self, 'additional_info'):
                stream += pack("%ds" % len(self.additional_info), self.additional_info)
        return stream


######################################################################
# TABLA NIT
def ni_section(nit_v, tvd_service_id_sd, tvd_orig_network_id, tvd_ts_id, network_name,
	area_code, guard_interval, transmission_mode, ts_freq, ts_remote_control_key):
	ns = len(tvd_service_id_sd)
	nit_dsdl = []
	nit_sil = []
	for i in range(0, ns):
		nit_dsdl.append(
			service_descriptor_loop_item (
				service_ID = tvd_service_id_sd[i],
				service_type = 0x19,
			)
		)
		nit_sil.append(
			service_id_loop_item(
				service_id=tvd_service_id_sd[i]
			),
		)
	nit = network_information_section(
		network_id = tvd_orig_network_id,
		network_descriptor_loop = [
			network_descriptor(network_name = network_name),
			system_management_descriptor(
				broadcasting_flag = 0,
				broadcasting_identifier = 3,
				additional_broadcasting_identification = 0x01,
				additional_identification_bytes = [],
			)
		],
		transport_stream_loop = [
			transport_stream_loop_item(
				transport_stream_id = tvd_ts_id,
				original_network_id = tvd_orig_network_id,
				transport_descriptor_loop = [
					service_list_descriptor(
						dvb_service_descriptor_loop = nit_dsdl,
					),
					terrestrial_delivery_system_descriptor(
						area_code = area_code,
						guard_interval = guard_interval,
						transmission_mode = transmission_mode,
						frequencies = [
							tds_frequency_item(freq = ts_freq)
						],
					),
					partial_reception_descriptor (
						service_ids = []
					),
					transport_stream_information_descriptor (
						remote_control_key_id = ts_remote_control_key,
						ts_name = network_name,
						transmission_type_loop = [
							transmission_type_loop_item(
								transmission_type_info = 0x0F,
								service_id_loop = nit_sil,
							),
							transmission_type_loop_item(
								transmission_type_info = 0xAF,
								service_id_loop = [],
							),
						],
					)
				],
			),
		],
		version_number = nit_v,
		section_number = 0,
		last_section_number = 0,
	)
	return nit


######################################################################
# TABLA SDT
def sd_section(sdt_v, tvd_service_id_sd, svc_md, tvd_ts_id, tvd_orig_network_id):
	ns = len(tvd_service_id_sd)
	sdt_sl = []
	for i in range(0, ns):
		sdt_sl.append(
			service_loop_item(
				service_ID = tvd_service_id_sd[i],  	# ID Servicio
				EIT_schedule_flag = 0,
				EIT_present_following_flag = 0,
				running_status = 4,
				free_CA_mode = 0,
				service_descriptor_loop = [
					service_descriptor(
						service_type = 0x19,	# Servicio de television digital avanzado
						service_provider_name = svc_md[i]['np'],
						service_name = svc_md[i]['n'],
					),
				],
			),
		)
	sdt = service_description_section(
		transport_stream_id = tvd_ts_id,
		original_network_id = tvd_orig_network_id,
		service_loop = sdt_sl,
		version_number = sdt_v,
		section_number = 0,
		last_section_number = 0,
	)
	return sdt

######################################################################
# TABLA PAT
def pa_section(pat_v, tvd_service_id_sd, tvd_pmt_pid_sd, tvd_ts_id):
	ns = len(tvd_service_id_sd)
	pat_pl = [
		# Programa especial para la tabla NIT
		program_loop_item(
			program_number = 0,
			PID = nit_pid,			    # ID de la tabla NIT
		),
	]
	for i in range(0, ns):
		pat_pl.append(
			# Programa para la tabla PMT i-ésima
			program_loop_item(
				program_number = tvd_service_id_sd[i],
				PID = tvd_pmt_pid_sd[i],
			),
		)
	pat = program_association_section(
		transport_stream_id = tvd_ts_id,
		program_loop = pat_pl,
		version_number = pat_v,
		section_number = 0,
		last_section_number = 0,
	)
	return pat

######################################################################
# TABLA AIT
def ai_section(ait_v, app_par, app_md):
	na = len(app_par)
	ait_al = []
	for i in range(0, na):
		ait_al.append(
			application_loop_item(
				organisation_id = app_md[i]['organisation_id'],
				application_id  = app_md[i]['id'],
				application_control_code = app_md[i]['control_code'],
									# Some required application descriptor follows application id
				application_descriptors_loop = [
					transport_protocol_descriptor(
						protocol_id = 0x0001,			# the application is broadcasted on a MHP DSMCC
						transport_protocol_label = 0,		# carousel id
						remote_connection = 0,
						component_tag = app_par[i]['component_tag'],	# carousel common tag and association tag
					),
					application_descriptor(
						application_profile = 0x0001,	# Profile and MHP version of the application MHP 1.0.0
						version_major = 1,
						version_minor = 0,
						version_micro = 0,
						service_bound_flag = 1,		# 1 means the application is expected to die on service change
						visibility = 3,			# 3 the applications is visible to the user,
										# 1 the application is visible only to other applications
						application_priority = 1,	# 1 is lowest, it is used when more than 1 applications is executing
						transport_protocol_labels = [ 0 ],	# carousel Id
					),
					application_name_descriptor(
						application_name = app_md[i]['name']
					),
					#ginga_ncl_application_descriptor(
					#	parameters = [ ]
					#),
					ginga_ncl_application_location_descriptor (
						base_directory = "/",		# base directory, if set to "/hello" the xlet will act as "/hello" is its root directory
						class_path_extension = "",	# an additiona classpath inside the carousel can be specified
						initial_class = app_md[i]['initial_class'],	# nombre del archivo NCL a ser ejecutado.
					),
				]
			),
		)
	ait = application_information_section(
		application_type = 0x0009,	 			# GINGA-NCL
		common_descriptor_loop = [],
		application_loop = ait_al,
		version_number = ait_v,
		section_number = 0,
		last_section_number = 0,
	)
	return ait

######################################################################
# TABLA PMT
def pm_section(pmt_sd_v, tvd_service_id_sd, pmt_par, ait_pid, ait_v, app_md):
	pm_sl = [
		# Stream de Video
		stream_loop_item(
			stream_type = 0x1b, 		# avc video stream type
			elementary_PID = pmt_par['pid_video'],
		element_info_descriptor_loop = [
			]
		),
		# Stream de Audio
		stream_loop_item(
			stream_type = 0x0f, 		# mpeg2 AAC audio stream type
			elementary_PID = pmt_par['pid_audio'],
			element_info_descriptor_loop = []
		),
	]
	if pmt_par['app_par']:
		pm_sl.append(
			# Stream tabla AIT
			stream_loop_item(
				stream_type = 5, 		# AIT stream type
				elementary_PID = ait_pid,
				element_info_descriptor_loop = [
					data_component_descriptor (
						data_component_id	= 0xA3, 				# sistema AIT
						additional_data_component_info = ait_identifier_info(
							application_type = GINGA_NCL_application_type,		
							ait_version	= ait_v
						).bytes(),
					),
					application_signalling_descriptor(
						application_type	= GINGA_NCL_application_type,
						AIT_version		= ait_v,
					),
				]
			),
		)
		for i in range(0, len(pmt_par['app_par'])):
			pm_sl.append(
				# Stream para Carrusel
				stream_loop_item(
					stream_type = 0x0b, 		# DSMCC stream type
					elementary_PID = pmt_par['app_par'][i]['pid_carrusel'],
					element_info_descriptor_loop = [
						association_tag_descriptor(
							association_tag = pmt_par['app_par'][i]['component_tag'],
							use = 0,
							selector_lenght = 0,
							transaction_id = 0x80000000,
							timeout = 0xFFFFFFFF,
							private_data = "",
						),
						stream_identifier_descriptor(
							component_tag = pmt_par['app_par'][i]['component_tag'],
						),
						carousel_identifier_descriptor(
							carousel_ID = pmt_par['app_par'][i]['id_carrusel'],
							format_ID = 0,
							private_data = "",
						),
						data_component_descriptor (
							data_component_id = 0xA0, 					# sistema GINGA
							additional_data_component_info = additional_ginga_j_info(
								transmission_format	= 0x2,
								document_resolution	= 0x5,
								organization_id		= app_md[i]['organisation_id'],
								application_id		= app_md[i]['id'],
								carousel_id		= pmt_par['app_par'][i]['id_carrusel'],
							).bytes(),
						),
					]
				)
			)
	pmt_sd = program_map_section(
		program_number = tvd_service_id_sd,
		PCR_PID = pmt_par['pid_video'],
		program_info_descriptor_loop = [],
		stream_loop = pm_sl,
		version_number = pmt_sd_v,
		section_number = 0,
		last_section_number = 0,
	)
	return pmt_sd
