$(document).ready(function(){

$('#menu').collapse();

$('#toggleMenu').on('click', function() {
    $('.sidebar').toggleClass('closed d-none d-sm-block d-block', 600, "easeOutSine");
    $('.content').toggleClass('col-sm-10 col-sm-12 margin-content', 550, "easeOutSine");
});

var table = $('#table').DataTable({
    language: {
        sEmptyTable: "Nenhum registro encontrado",
        sInfo: "Mostrando de _START_ até _END_ de _TOTAL_ registros",
        sInfoEmpty: "Mostrando 0 até 0 de 0 registros",
        sInfoFiltered: "(Filtrados de _MAX_ registros)",
        sInfoPostFix: "",
        sInfoThousands: ".",
        sLengthMenu: "_MENU_",
        sLoadingRecords: "Carregando...",
        sProcessing: "Processando...",
        sZeroRecords: "Nenhum registro encontrado",
        sSearch: "",
        oPaginate: {
        sNext: "Próximo",
        sPrevious: "Anterior",
        sFirst: "Primeiro",
        sLast: "Último",
        },
        oAria: {
            sSortAscending: ": Ordenar colunas de forma ascendente",
            sSortDescending: ": Ordenar colunas de forma descendente",
            },
        }
});

$('#search').on( 'keyup', function () {
    table.search( this.value ).draw();
});

$( ".col-sm-12:has(> table)" ).addClass( "col-no-padding" );

});

function isNull(valor) {
	return valor == undefined || valor == null || $.trim(valor) == '' || valor == 'None';
}