import paramiko

paramiko.util.log_to_file('paramiko.log')
HOST = '192.168.12.197'
PUERTO = 22
USUARIO = 'cenditel'
datos = dict(hostname=HOST, port=PUERTO, username=USUARIO)
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(**datos)
entrada, salida, error = ssh_client.exec_command('pwd')
ruta = salida.read().replace('\n', '')

sftp = ssh_client.open_sftp() # Crea un objeto SFTPClient()

# Descargando archivos
archivos = sftp.listdir()
for archivo in archivos:
	archivo_remoto = "%(ruta)s/%(nombre)s" % dict(ruta='/tmp', nombre='0000000A0050.zip')
	print "Descargando: %s" % archivo_remoto
	try:
		sftp.get(archivo_remoto, "/var/local/cumaco/" % archivo)
		print "copiado archivo %s." % archivo
	except:
		print "Fallo al intentar copiar %s. Tal vez es un directorio." % archivo

sftp.close()
ssh_client.close()