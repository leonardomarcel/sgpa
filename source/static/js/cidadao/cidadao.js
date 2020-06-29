
$(document).ready(function() {
	onChangeTipoDocumento();
});

function onChangeTipoDocumento() {
	$("#id_tipo_documento").change(function (){
		var valor = $(this).val();
		
		if(valor == 'CPF') {
			$("#id_tipo_documento_numero").mask('999.999.999-99');
		} else {
			$("#id_tipo_documento_numero").unmask();
		}
	});
}