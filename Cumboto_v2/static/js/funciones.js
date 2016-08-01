/**
 * @brief Función que mide la fortaleza de la contraseña y la muestra en pantalla
 * @param password Cadena de carácteres con la contraseña indicada por el usuario
 */
function passwordStrength(password) {
    var desc = new Array();
    desc[0] = MSG_PASSWD_MUY_DEBIL;
    desc[1] = MSG_PASSWD_DEBIL;
    desc[2] = MSG_PASSWD_REGULAR;
    desc[3] = MSG_PASSWD_BUENA;
    desc[4] = MSG_PASSWD_FUERTE;
    desc[5] = MSG_PASSWD_MUY_FUERTE;

    var score   = 0;

    //if password bigger than 6 give 1 point
    if (password.length > 6) score++;

    //if password has both lower and uppercase characters give 1 point
    if ( ( password.match(/[a-z]/) ) && ( password.match(/[A-Z]/) ) ) score++;

    //if password has at least one number give 1 point
    if (password.match(/\d+/)) score++;

    //if password has at least one special caracther give 1 point
    if ( password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/) ) score++;

    //if password bigger than 12 give another 1 point
    if (password.length > 12) score++;

     document.getElementById("passwordDescription").innerHTML = desc[score];
     document.getElementById("passwordStrength").className = "strength" + score;
     document.getElementById("passwordMeterId").value = score;
}

/**
 * @brief Función que muestra una ventana emergente con el formulario de selección para el año de registro
 * @param title Titulo de la ventana emergente
 * @param template Plantilla html a utilizar para mostrar el formulario
 */
function anho_registro(title, template) {
    var modal = bootbox.dialog({
        title: title,
        message: template,
        buttons: {
            success: {
                label: BTN_REGISTRAR,
                className: "btn btn-primary btn-sm",
                callback: function() {

                }
            },
            'limpiar': {
                label: BTN_LIMPIAR,
                className: "btn btn-success btn-sm",
                callback: function() {
                    $(modal).find("form")[0].reset();
                    return false;
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        }
    });

    $(modal).find('#anhoregistro').html("<option value=''>" + SELECT_INICIAL_DATA + "</option>");
    var anho_actual = new Date();
    for (i=ANHO_REGISTRO_INICIAL; i<=anho_actual.getFullYear(); i++) {
        $(modal).find('#anhoregistro').append("<option '" + i + "'>" + i + "</option>");
    }
    $(modal).find('.select2').select2({});
}

/**
 * @brief Función que muestra una ventana emergente con un mapa para la selección de las coordenadas geográficas
 * @param title Titulo de la ventana emergente
 * @param template Plantilla html a utilizar para mostrar el formulario
 */
function seleccionar_coordenadas(title, template) {
    var modal = bootbox.dialog({
        title: title,
        message: template,
        buttons: {
            success: {
                label: BTN_AGREGAR,
                className: "btn btn-primary btn-sm",
                callback: function() {
                    $("#id_coordenada_0").val($(modal).find("#inputLongitud").val());
                    $("#id_coordenada_1").val($(modal).find("#inputLatitud").val());
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        },
        show: false //Por defecto no se muestra la ventana modal al invocarla para poder cargar el mapa
    });
    $(modal).on("shown.bs.modal", function() {
        /* Carga el mapa cuando la ventana modal es mostrada */
        load_map();
    });
    /* Muestra la ventana de dialogo modal despues de haber cargado el mapa en su correspondiente div */
    $(modal).modal("show");
}

/**
 * @brief Función que carga los datos del mapa a mostrar para la selección de coordenadas geográficas
 */
function load_map() {
    $(document).ready(function() {
        var app = {};

        /**
         * @constructor
         * @extends {ol.interaction.Pointer}
         */
        app.Drag = function() {
            ol.interaction.Pointer.call(this, {
                handleDownEvent: app.Drag.prototype.handleDownEvent,
                handleDragEvent: app.Drag.prototype.handleDragEvent,
                handleMoveEvent: app.Drag.prototype.handleMoveEvent,
                handleUpEvent: app.Drag.prototype.handleUpEvent
            });

            /**
             * @type {ol.Pixel}
             * @private
             */
            this.coordinate_ = null;

            /**
             * @type {string|undefined}
             * @private
             */
            this.cursor_ = 'pointer';

            /**
             * @type {ol.Feature}
             * @private
             */
            this.feature_ = null;

            /**
             * @type {string|undefined}
             * @private
             */
            this.previousCursor_ = undefined;
        };

        ol.inherits(app.Drag, ol.interaction.Pointer);

        /**
         * @param {ol.MapBrowserEvent} evt Map browser event.
         * @return {boolean} `true` to start the drag sequence.
         */
        app.Drag.prototype.handleDownEvent = function(evt) {
            var map = evt.map;

            var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                return feature;
            });

            if (feature) {
                this.coordinate_ = evt.coordinate;
                this.feature_ = feature;
            }

            return !!feature;
        };

        /**
         * @param {ol.MapBrowserEvent} evt Map browser event.
         */
        app.Drag.prototype.handleDragEvent = function(evt) {
            var deltaX = evt.coordinate[0] - this.coordinate_[0];
            var deltaY = evt.coordinate[1] - this.coordinate_[1];

            var geometry = (this.feature_.getGeometry());
            geometry.translate(deltaX, deltaY);
            $("#inputLongitud").val(evt.coordinate[0]);
            $("#inputLatitud").val(evt.coordinate[1]);

            this.coordinate_[0] = evt.coordinate[0];
            this.coordinate_[1] = evt.coordinate[1];
        };

        /**
         * @param {ol.MapBrowserEvent} evt Event.
         */
        app.Drag.prototype.handleMoveEvent = function(evt) {
            if (this.cursor_) {
                var map = evt.map;
                var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
                    return feature;
                });
                var element = evt.map.getTargetElement();

                if (feature) {
                    if (element.style.cursor != this.cursor_) {
                        this.previousCursor_ = element.style.cursor;
                        element.style.cursor = this.cursor_;
                    }
                } else if (this.previousCursor_ !== undefined) {
                    element.style.cursor = this.previousCursor_;
                    this.previousCursor_ = undefined;
                }
            }
        };

        /**
         * @return {boolean} `false` to stop the drag sequence.
         */
        app.Drag.prototype.handleUpEvent = function() {
            this.coordinate_ = null;
            this.feature_ = null;
            return false;
        };

        var satellite = new ol.layer.Tile({
            source: new ol.source.MapQuest({layer: 'sat'})
        });

        var osm = new ol.layer.Tile({
            source: new ol.source.MapQuest({layer: 'osm'})
        });

        var iconGeometry = new ol.geom.Point([-65.0000,6.5000]).transform('EPSG:4326', 'EPSG:3857');

        var pointFeature = new ol.Feature({
            geometry: iconGeometry,
            name: 'Mark'
        });

        var iconStyle = new ol.style.Style({
            image: new ol.style.Icon(({
                anchor: [0.5, 15], // Posicion del icono en el eje X Y
                anchorXUnits: 'fraction', // Unidad de medida para el posicionamiento del icon en el eje X
                anchorYUnits: 'pixels', // Unidad de medida para el posicionamiento del icon en el eje X
                //opacity: 0.75,
                src: URL_STATIC_FILES+'img/mark.png',
                // the scale factor
                scale: 1.1 // Tamaño de la imagen de acuerdo a la escala en base al tamaño original
            }))
        });

        pointFeature.setStyle(iconStyle);

        var vectorLayer = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: [pointFeature]
            })
        });

        var map = new ol.Map({
            interactions: ol.interaction.defaults().extend([new app.Drag()]),
            target: 'map',
            layers: [satellite, osm, vectorLayer],
            view: new ol.View({
                center: ol.proj.transform([-65.0000,6.5000], 'EPSG:4326', 'EPSG:3857'),
                zoom: 4
            })
       });

        var mousePosition = new ol.control.MousePosition({
            coordinateFormat: ol.coordinate.createStringXY(6),
            projection: 'EPSG:3857',
            target: document.getElementById('myposition'),
            undefinedHTML: '&nbsp;'
        });

        map.on('singleclick', function(evt) {
            $("#inputLongitud").val(evt.coordinate[0]);
            $("#inputLatitud").val(evt.coordinate[1]);
            // Modifica la posición actual del marcador al hacer click sobre un punto en el mapa
            iconGeometry.setCoordinates(evt.coordinate);
            //console.log(evt.pixel);
        });

        map.addControl(mousePosition);

        map.on('loadstart', function() {
            cargando.showPleaseWait();
        });

        map.on('loadend', function() {
            cargando.hidePleaseWait();
        });

        map.updateSize();
    });
}

/**
 * @brief Función que habilita los campos dependientes de un select
 * @param opcion Respuesta del usuario según la pregunta
 * @param campo Campo a deshabilitar
 */
function habilitar(opcion, campo){
    if((opcion == "S") || (opcion == "Otro") || (opcion == "1")){
        $('#'+campo).removeAttr('disabled');
    }else{
        $('#'+campo).attr('disabled', 'disabled');
        $('#'+campo).val("");
    }
}

/**
 * @brief Función que habilita los campos dependientes de un select
 * @param opcion Respuesta del usuario según la pregunta
 * @param campo Campo a deshabilitar
 */
function deshabilitar(opcion, campo){
    if(opcion == "1"){
        $('#'+campo).attr('disabled', 'disabled');
        $('#'+campo).val("");
    }else{
        $('#'+campo).removeAttr('disabled');
    }
}

/**
 * @brief Función para agregar campos a un datatable
 * @param campos Es un arreglo con el id de los campos a agregar en la tabla
 * @param table_id Es un campo con el id de la tabla en la que agregan los campos
 */
function add_field_datatable(campos, table_id){
    var bool = true;
    var new_data = new Array();
    var t = $(table_id).DataTable();
    var index = t.rows()[0].length;
    $.each(campos,function(index,value){
            var text = $(value).val();
            var form = "<input type='text' id="+value.replace('#','')+"_tb value='"+text+"' name="+value.replace('#id_','')+"_tb hidden='true' >";
            if((text.trim()==''))
            {
                bool = false
            }
            if ($(value+" option:selected").text()) {
                text = $(value+" option:selected").text();
            }
            new_data.push(text+form);
        });
    if (!bool) {
        var modal = bootbox.dialog({
            title: 'Alerta',
            message: 'Algunos campos estan vacios',
            buttons: {
                main: {
                    label: 'Aceptar',
                    className: "btn btn-primary btn-sm"
                }
            }
        });
        modal.show();
        new_data = [];
    }
    else
    {
        $.each(campos,function(index,value){
            $(value).val('');
        });
        var buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>';
        buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>';
        new_data.push(buttons);
        t.row.add(new_data).draw(false);
    }
}

/**
 * @brief Remover dinámicamente campos de una datatable con el id mydtable
 * @param table_id Es un campo con el id de la tabla en la que se eliminaran los campos
 */
function remove_field_datatable(table_id) {
    $(table_id).on('click','.remove_item',function(){
        var t = $(table_id).DataTable();
        var myrow = t.row($(this).parent().closest('tr'));
        var modal = bootbox.dialog({
            title: 'Eliminar Campos',
            message: "¿Está seguro que desa eliminar la fila seleccionada?",
            buttons: {
                success: {
                    label: 'Aceptar',
                    className: "btn btn-primary btn-sm",
                    callback: function() {
                        myrow.remove().draw( false );
                    }
                },
                main: {
                    label: BTN_CANCELAR,
                    className: "btn btn-warning btn-sm"
                }
            },
        });
        modal.show();
    });
}

/**
 * @brief Actualiza dinámicamente campos de una datatable con el id mydtable
 * @param table_id Es un campo con el id de la tabla en la que se actualizaran los campos
 * @param view Campo que hace referencia al script html que esta en base.form.box.html
 * @param campos Es un array con los campos que se manipularan en el modal
 */
function update_field_datatable(table_id,view,campos) {
    var mensaje = '';
    $(table_id).on('click','.update_item',function(){
        var tr = $(this).parent().closest('tr');
        var t = $(table_id).DataTable();
        mensaje = $(view).html();
        var modal = bootbox.dialog({
        title: 'Actualizar Campos',
        message: mensaje,
        buttons: {
            success: {
                label: 'Actualizar',
                className: "btn btn-primary btn-sm",
                callback: function() {
                    var bool = true;
                    var new_data = [];
                    $.each(campos,function(index,value){
                        var text = $(modal).find(value).val();
                        var form = "<input type='text' id="+value.replace('#','')+"_tb value='"+text+"' name="+value.replace('#id_','')+"_tb hidden='true' >";
                        if((text.trim()==''))
                        {
                            $(modal).find(value).parent().closest('.form-group').addClass('has-error');
                            bool = false
                        }
                        if ($(modal).find(value +" option:selected").text()) {
                            text = $(modal).find(value +" option:selected").text();
                        }
                        new_data.push(text+form);
                    });
                    if (!bool) {
                        alert("Algún campo esta incompleto");
                        return false;
                    }
                    else{
                        var buttons = '<a class="update_item" style="cursor: pointer"><i class="glyphicon glyphicon-pencil"></i></a>';
                        buttons += '<a class="remove_item" style="cursor: pointer"><i class="glyphicon glyphicon-remove"></i></a>';
                        new_data.push(buttons);
                        t.row(tr).remove().draw(false);
                        t.row.add(new_data).draw(false);
                    }
                }
            },
            main: {
                label: BTN_CANCELAR,
                className: "btn btn-warning btn-sm"
            }
        },
        });
        $.each(tr.find('input'),function(index,value){
            $(modal).find(campos[index]).html($(campos[index]).html());
            $(modal).find(campos[index]).val($(value).val());
        });
        modal.show();
    });
}

/**
 * @brief Función para ocultar campos de una datable
 * @param table_id Es un campo con el id de la tabla en la que se ocultaran los campos
 * @param fields Es un arreglo con el id de los campos a ocultar en la tabla
 */
function default_datatable_field(table_id,fields) {
    var t = $(table_id).DataTable();
    $.each(fields,function(index,value){
       var col = t.column(value);
       col.visible(false);
    });
}