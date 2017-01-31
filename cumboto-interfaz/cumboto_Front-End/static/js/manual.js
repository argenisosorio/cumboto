/*Manual de Usuario Dinamico CUMBOTOV2*/
/*!
 * @autor: HUGO ALEJANDRO RAMIREZ MORENO
 * Copyright CENDITEL
 * Date: 2016-10-26 T14:20Z
 */

/* Funcion Que LLama Al Modal Que Contiene La Descripcion Del Modulo Gestion De Usuario */
$(document).ready(function(){
	$("#BtnUsuario").click(function(){
		$("#ModalUsuario").modal();
	});
});

/* Funcion Que LLama Al Modal Que Contiene La Descripcion Del Modulo Biblioteca */
$(document).ready(function(){
	$("#BtnBiblioteca").click(function(){
		$("#ModalBiblioteca").modal();
	});
});

/* Funcion Que LLama Al Modal Que Contiene La Descripcion Del Modulo Configuración De Servicios */
$(document).ready(function(){
	$("#BtnServicios").click(function(){
		$("#ModalServicios").modal();
	});
});

/* Funcion Que LLama Al Modal Que Contiene La Descripcion Del Modulo Agenda */
$(document).ready(function(){
	$("#BtnAgenda").click(function(){
		$("#ModalAgenda").modal();
	});
});