### SISTEMA DE GESTIÓN PARA LA TRANSMISIÓN DE APLICACIONES INTERACTIVAS DESDE LA
SALA DE CONTROL MAESTRO DE UNA ESTACIÓN DE TELEVISIÓN ###

Se trata de un sistema informático que proporcione una interfaz gráfica que permita
controlar de forma sencilla y expedita la transmisión del contenido interactivo
de un canal de Televisión Digital Abierta, de manera que en todo momento se
mantenga congruente con la programación del canal y con su estrategia comunicacional.
Esa interfaz habrá de estar diseñada para ser manejada desde la sala de control
maestro del canal por parte del personal técnico asignado a ella.

### Licencia ###

CUMBOTO-v2, sus carpetas y archivos, se disribuye bajo la Licencia de Software
Libre GNU/GPL versión 2, esto implica que el usuario final de la aplicación esta
en la libertad de ejecutarla, modificar su código fuente, copiarla y/o
distribuírla, siempre y cuando al hacerlo se citen las fuentes originales de ésta
aplicación.

Para obtener mayor información en torno a los términos de la licencia bajo los
cuales se distribuye la aplicación, lea con atención la
GPLv2 --> http://www.gnu.org/licenses/gpl-2.0.html.

Así mismo, las librerías y apis de terceros implementadas en esta aplicación, se
distribuyen con sus respectivas licencias y acuerdos particulares de cada una
especificadas en los archivos de esas librerías.

La documentacion detallada sobre como funciona la aplicacion, la puede encontrar
en la direccion: --> https://cumaco.cenditel.gob.ve/desarrollo/wiki/PropuestaDesarrollo2016.

El API-REST es la segunda capa del sistema cumboto, esta permite la cumunicacion
directa entre el servidor de transmision y la interfaz grafica

### Pre-requisitos ###

Para el correcto funcionamiento de la  API-REST se requiere tener instalado
previamente los siguientes paquetes:

En el proceso de instalación sobre los requerimientos y herramientas necesarias
para el correcto funcionamiento del sistema, se deben ejecutar algunas instrucciones
desde la consola de comandos para lo cual se requiere abrir una terminal y ejecutar
los siguiente:

$ su

Lo anterior solicitara la contraseña de administrador del sistema operativo para
acceder al usuario root, esto es necesario para los procesos de instalación
posteriores de la aplicación.

Una vez autenticados como usuario root del sistema operativo, mostrará en la consola
el símbolo "#" que identifica que el usuario actual es root, esto permitirá instalar
en el sistema operativo los requerimientos de funcionamiento del sistema para lo
cual se ejecutarán los comandos detallados a continuación:

### Instalación de paquetes de python accediendo a la ruta principal del
proyecto (API-REST_Back-end/) ###

# pip install -r requirements/base.txt
    
Esto ejecutara los distintos procesos de instalación sobre los requerimientos
del sistema.

### Instalación de Ocumare ###

1-) Instalar las siguientes paquetes:

# pip install filelock==2.0.7

2-) Descargar código fuente desde el trac de CENDITEL:

# export GIT_SSL_NO_VERIFY=True
# cd /usr/local/src/
# git clone https://cumaco.cenditel.gob.ve/desarrollo/scm/git/ocumare.git

3-) Crear los directorios donde se encontraran los archivos de configuración del
sistema, archivos de transmisión y la biblioteca de aplicaciones:

• Archivo de configuración del sistema de transmisión:
# mkdir /etc/cumaco

• Archivos de configuración y transport stream (TS) a transmitir:
# mkdir -p /var/local/cumaco/biblio

• Biblioteca donde se hospedarán las aplicaciones interactivas:
# mkdir /var/local/cumaco/transmision

4-) Copiar los archivos de configuración desde la carpeta “doc” del codigo fuente hacia los directorios de trabajo:

• Copiar el archivo de configuración del sistema de transmisión:
# cp -r /usr/local/src/ocumare/doc/ocumare.conf /etc/cumaco

• Copiar los archivos de configuración y transport stream (TS) a transmitir:
# cp -r /usr/local/src/ocumare/doc/transmision/* /var/local/cumaco/transmision

•  Copiar ejemplo o estructura de las biblioteca donde se hospedan las aplicaciones interactivas:
# cp -r /usr/local/src/ocumare/doc/biblio/* /var/local/cumaco/biblio

5-). Para entornos de pruebas de Ocumare, se puede ejecutar por medio del script gtsco.py:

# cd /usr/local/bin
# ln -s /usr/local/src/ocumare/luth/gtsco.py

### Instalación de Opencaster 3.2.2 ###

### Desde Repositorio de Debian Jessie ###

1-) Instalar el siguiente paquete:

# aptitude install opencaster

### Desde el repositorio de CENDITEL ####

1. Dependencias:
libc6 (>= 2.17)
libdvbcsa1 (>= 1.1.0)
zlib1g (>= 1:1.1.4)
python (>= 2.7)
python (< 2.8)
libdvbcsa-dev

2-) Instalar las siguientes dependencias:

# aptitude install python-all-dev libdvbcsa1 libdvbcsa-dev debhelper
# aptitude install build-essential devscripts
# aptitude -R install binutils gcc libc6-dev libgomp1 linux-libc-dev make python-dev \
 *python2.5-dev* zlib1g-dev python-dateutil

3-) Descargar código fuente desde el trac de Cumaco-CENDITEL
# export GIT_SSL_NO_VERIFY=True
# cd /usr/local/src/
# git clone https://cumaco.cenditel.gob.ve/desarrollo/scm/git/opencaster.git

4-) Construir el paquete Debian de opencaster e instalar:
    4.1. En el directorio del paquete opencaster-3.2.2/opencaster-3.2.1+dfsg ejecutar:
    $ debuild -us -uc -b
    4.2. Luego de que la construcción del paquete sea exitosa, instalar (desde la cuenta de superusuario):
    # dpkg -i opencaster_3.2.2+dfsg-1_amd64.deb
    4.3. Realizar los siguientes enlaces simbólicos, esto se debe a que cambiaron el nombre en esta versión.
    # ln -s /usr/bin/file2mod /usr/bin/file2mod.py
    # ln -s /usr/bin/mod2sec /usr/bin/mod2sec.py
    # ln -s /usr/bin/oc-update /usr/bin/oc-update.py

Para ejecutar la aplicación en modo de desarrollo, se debe ejecutar el siguiente comando:

$ python manage.py runserver mas la direccion IP y el puerto por el cual estar el web service a la escucha

$ python manage.py runserver IP:PORT

Lo anterior ejecutará el servidor de desarrollo de django bajo la URL [http://IP:PORT](http://IP:PORT), por el cual se recibiran las peticiones y se dara respuesta. Esta debe coinsidir con la ip configurada en el settings.py en el Frontend en la variable URL_API_REST =  'http://xxx.xxx.xxx.xxx:port/'
