<<<<<<< HEAD
====
CAPA DE ENLACE
====
       ######## #####      ###              ###   #####  ##       #  #####  ###### ###### ########   
          ##    ##   ##  ##   ##          ##   ## ##   # ##      #   ##   # ##     ##        ##      
          ##    ##    ## #######  ######  ####### #####  ##     #    #####  ####   ######    ##      
          ##    ##   ##  ##   ##          ##   ## ##     ##    #     ##  ## ##         ##    ##      
          ##    #####    ##   ##          ##   ## ##     ##   #      ##  ## ###### ######    ##      

API-REST: Se basa el la segunda capa del sistema cumboto esta permite la cumunicacion directa entre el servidor de transmision y la interfaz grafica

La documentacion detallada sobre como funciona la aplicacion, la puede encontrar en la direccion: https://cumaco.cenditel.gob.ve/desarrollo/wiki/PropuestaDesarrollo2016.


Inicio Rapido
-------------

1. Modifica el archivo `settings.py` con los datos de la base de datos a utilizar.

2. Ejecuta el servidor de desarrollo: `python manage.py runserver IP:PORT`.

3. Accede a la aplicacion, desde un navegador, median la URL http://IP:PORT 
=======
### Documentación - Cumboto-V2.0 ###

### SISTEMA DE GESTIÓN PARA LA TRANSMISIÓN DE APLICACIONES INTERACTIVAS DESDE
LA SALA DE CONTROL MAESTRO DE UNA ESTACIÓN DE TELEVISIÓN REQUIERE DE UN WEB
SERVICE EL CUAL LLAMAMOS CAPA DE ENLACE API-REST ###

Se basa el la segunda capa del sistema cumboto esta permite la cumunicacion directa entre el servidor de transmision y la interfaz grafica

### Pre-requisitos ###

Para el correcto funcionamiento de la  API-REST se requiere tener instalado previamente los siguientes paquetes:

### Paquetes del Sistema Operativo ###

python >= 3.4
PIP3 >= 8.1.1

### Paquetes de Python ###

djangorestframework
coreapi (1.32.0+)
Markdown (2.1.0+)
django-filter (0.9.2+)
django-crispy-forms 
django-guardian (1.1.1+)
Django >= 1.9.5 <1.10


### Proceso de instalación ###

En el proceso de instalación sobre los requerimientos y herramientas necesarias para el correcto funcionamiento del 
sistema, se deben ejecutar algunas instrucciones desde la consola de comando para lo cual se requiere abrir una terminal 
y ejecutar los siguientes comandos:

### Para distribuciones ubuntu ###

$ sudo su -
    
### Para distribuciones debian ###

$ su -

Lo anterior solicitara la contraseña de administrador del sistema operativo para acceder al usuario root, esto es necesario para los procesos de instalación posteriores de la aplicación.

Una vez autenticados como usuario root del sistema operativo, mostrará en la consola el símbolo "#" que identifica que el usuario actual es root, esto permitirá instalar en el sistema operativo los requerimientos de funcionamiento del sistema para lo cual se ejecutarán los comandos detallados a continuación:

### Instalación de paquetes rest-framework ###

pip install djangorestframework
pip install markdown
pip install django-filter  

### Instalación de paquetes de python (se debe acceder a la ruta principal del proyecto) ###

# pip install -r requirements/base.txt
    
Esto ejecutara los distintos procesos de instalación sobre los requerimientos del sistema.

Para ejecutar la aplicación en modo de desarrollo, se debe ejecutar el siguiente comando:

$ python manage.py runserver IP:PORT

Lo anterior ejecutará el servidor de desarrollo de django bajo la URL [http://IP:PORT](http://IP:PORT), por el cual se recibiran las peticiones y se dara respuesta. Esta debe coinsidir con la ip configurada en el settings.py en el Frontend en la variable URL_API_REST =  'http://xxx.xxx.xxx.xxx:port/'

### Documentación ###

Para acceder a la documentación del sistema, en donde se especifiquen las clases, funciones, atributos y métodos 
utilizados en la aplicación, debe abrir cada archivo .py donde el mismo presentara la descripcion que corresponda.
>>>>>>> desarrollo
