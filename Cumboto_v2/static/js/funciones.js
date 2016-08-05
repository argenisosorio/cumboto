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