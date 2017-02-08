Documentación - Cumboto-V2.0

### SISTEMA DE GESTIÓN PARA LA TRANSMISIÓN DE APLICACIONES INTERACTIVAS DESDE LA SALA DE CONTROL MAESTRO DE UNA ESTACIÓN DE TELEVISIÓN ###

SISTEMA DE GESTIÓN PARA LA TRANSMISIÓN DE APLICACIONES INTERACTIVAS DESDE LA SALA DE CONTROL MAESTRO DE UNA ESTACIÓN DE TELEVISIÓN. Se trata de un sistema informático que proporcione una interfaz gráfica que permita controlar de forma sencilla y expedita la transmisión del contenido interactivo de un canal de Televisión Digital Abierta, de manera que en todo momento se mantenga congruente con la programación del canal y con su estrategia comunicacional. Esa interfaz habrá de estar diseñada para ser manejada desde la sala de control maestro del canal por parte del personal técnico asignado a ella.

### Licencia ###

CUMBOTO-v2, sus carpetas y archivos, se disribuye bajo la Licencia de Software Libre GNU/GPL versión 2, esto implica que el usuario final de la aplicación esta en la libertad de ejecutarla, modificar su código fuente, copiarla y/o distribuírla, siempre y cuando al hacerlo se citen las fuentes originales de ésta aplicación.

Para obtener mayor información en torno a los términos de la licencia bajo los cuales se distribuye la aplicación, lea con atención la GPLv2 --> http://www.gnu.org/licenses/gpl-2.0.html.

Así mismo, las librerías y apis de terceros implementadas en esta aplicación, se distribuyen con sus respectivas licencias y acuerdos particulares de cada una especificadas en los archivos de esas librerías.

La documentacion detallada sobre como funciona la aplicacion, la puede encontrar en la direccion: --> https://cumaco.cenditel.gob.ve/desarrollo/wiki/PropuestaDesarrollo2016.

### Pre-requisitos ###

Para el correcto funcionamiento de CUMBOTO-V2 se requiere tener instalado previamente los siguientes paquetes:

-Paquetes del Sistema Operativo
	PostgreSQL 9.x
	Python >= 3.4
	PIP3 >= 8.1.1
    
-Paquetes de Python
	Django >= 1.9.5 <1.10
	psycopg2 >= 2.6.1
    
### Proceso de instalación ###

En el proceso de instalación sobre los requerimientos y herramientas necesarias para el correcto funcionamiento del sistema, se deben ejecutar algunas instrucciones desde la consola de comando para lo cual se requiere abrir una terminal y ejecutar los siguientes comandos:

-Para distribuciones ubuntu:
$ sudo su
    
-Para distribuciones debian
$ su

Lo anterior solicitara la contraseña de administrador del sistema operativo para acceder al usuario root, esto es necesario para los procesos de instalación posteriores de la aplicación.

Una vez autenticados como usuario root del sistema operativo, mostrará en la consola el símbolo "#" que identifica que el usuario actual es root, esto permitirá instalar en el sistema operativo los requerimientos de funcionamiento del sistema para lo cual se ejecutarán los comandos detallados a continuación:

-Instalación de paquetes del sistema operativo
# apt-get install postgresql postgresql-server-dev-all python3.4 python3-pip

-Instalación de paquetes del sistema operativo necesarios para la compilación de los requerimientos
# apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python3.4 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python3.4-dev libpq-dev

-Instalación de paquetes de python (se debe acceder a la ruta principal del proyecto)
# pip install -r requirements/base.txt

Esto ejecutara los distintos procesos de instalación sobre los requerimientos del sistema.

Posteriormente se debe crear la base de datos del CUMBOTO-V2 y el correspondiente usuario que tendrá los privilegios necesarios para interactuar con la misma, esto se hace de la siguiente forma:

-Acceso al usuario postgres
# su postgres

-Acceso a la interfaz de comandos de postgresql
postgres@xxx:$ psql template1

-Creación del usuario de a base de datos
temlate1=# CREATE USER nombre_usuario_bd WITH ENCRYPTED PASSWORD 'contraseña' createdb;
temlate1=# \q

-Desautenticar el usuario postgres y regresar al usuario root
postgres@xxx:$ exit

-Creación de la base de datos
# createdb nombre_bd -E 'UTF-8' -O nombre_usuario_bd -h localhost -p 5432 -U nombre_usuario_bd

-Salir del usuario root
# exit

### Configuración y ejecución de la aplicación ###

Configuracion del web service en la carpeta cumboto en el archivo settings se debe configurar la variable global URL_API_REST donde se configura la ip y el puerto del api-rest o el web service.

Una vez instalados todos los requerimientos previos del sistema, se procede a la configuración del mismo, para esto se debe editar el archivo settings.py dentro de la carpeta cumboto y modificar los datos por defecto de la variable DATABASES_CONFIG, que se encuentra ubicada en el archivo database_config.py en donde se especificarán los datos de acceso a las bases de datos de la aplicación.

Al tener ya configurado los parámetros de acceso a la base de datos, se ejecutan los siguiente comandos:

-Para construir las migraciones de la base de datos en caso de que no existan:
$ python manage.py makemigrations

-Para crear la estructura de la base de datos:
$ python manage.py migrate

Lo anterior crea la estructura de la base de datos e incorpora los registros básicos de la aplicación.

-Para ejecutar la aplicación en modo de desarrollo, se debe ejecutar el siguiente comando:s
$ python manage.py runserver
    
Lo anterior ejecutará el servidor de desarrollo de django bajo la URL [http://localhost:8000](http://localhost:8000), para lo cual deberemos acceder a un navegador web y escribir dicha dirección URL.

### Documentación del código fuente ###

Para acceder a la documentación del sistema, en donde se especifiquen las clases, funciones, atributos y métodos utilizados en la aplicación, debe abrir cada archivo .py donde el mismo presentara la descripcion que corresponda.

### Inicio Rapido ###

1-) Modifica el archivo settings.py con los datos de la base de datos a utilizar mas la variable URL_API_REST con la direccion ip y el puerto por el cual el api estara en ejecucion. URL_API_REST =  http://localhost:8888

2-) Ejecuta el comando para crear las migraciones de los modelos de datos:
$ python manage.py migrate

3-) Ejecuta el servidor de desarrollo:
$ python manage.py runserver

4-) Accede a la aplicacion, desde un navegador, median la URL http://localhost:8000
