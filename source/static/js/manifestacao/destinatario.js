var $selectizeAssunto
$(document).ready(function() {
	initializeSelectize();
	$selectizeAssunto = $("#id_1-assunto")[0].selectize;
	onChangeTipoAssunto();
});

function initializeSelectize() {
	$('select').selectize({
		maxItems: 1,
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		placeholder: 'Selecione...',
		selectOnTab: true,
	});
}

function onChangeTipoAssunto() {
	$("#id_1-tipo_assunto").change(function () {
		var id_tipo_assunto = $(this).val();
		
		if(id_tipo_assunto != null) {
			$selectizeAssunto.clearOptions();
			$selectizeAssunto.load(function(callback) {
	    		$.getJSON('/publico/assuntos_json/'+ id_tipo_assunto, function(data) {
					 callback(data);
				}).fail(function() {
					toastr.error('Ocorreu um problema ao tentar carregar os assuntos.', 'Assuntos');
				}).done(function() {
					$selectizeAssunto.enable();
				});
	    	});
		}
	});
}