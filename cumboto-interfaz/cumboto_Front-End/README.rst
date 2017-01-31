====
CUMBOTO-V2
====

SISTEMA DE GESTIÓN PARA LA TRANSMISIÓN DE APLICACIONES INTERACTIVAS DESDE LA SALA DE CONTROL MAESTRO DE UNA ESTACIÓN DE TELEVISIÓN. Se trata de un sistema informático que proporcione una interfaz gráfica que permita controlar de forma sencilla y expedita la transmisión del contenido interactivo de un canal de Televisión Digital Abierta, de manera que en todo momento se mantenga congruente con la programación del canal y con su estrategia comunicacional. Esa interfaz habrá de estar diseñada para ser manejada desde la sala de control maestro del canal por parte del personal técnico asignado a ella.

La documentacion detallada sobre como funciona la aplicacion, la puede encontrar en la direccion: https://cumaco.cenditel.gob.ve/desarrollo/wiki/PropuestaDesarrollo2016.


Inicio Rapido
-------------

1. Modifica el archivo `settings.py` con los datos de la base de datos a utilizar mas la variable URL_API_REST con la direccion ip y el puerto por el cual el api estara en ejecucion.  URL_API_REST =  http://localhost:8888

2. Ejecuta el comando `python manage.py migrate` para crear las migraciones de los modelos de datos.

3. Ejecuta el servidor de desarrollo: `python manage.py runserver`.

4. Accede a la aplicacion, desde un navegador, median la URL http://localhost:8000