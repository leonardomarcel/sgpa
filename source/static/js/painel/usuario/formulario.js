$(document).ready(function() {
	initializeSelectize();
	formMeuPerfilHasChanged();
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

function formMeuPerfilHasChanged() {
	$("#formPerfilGestor :input").change(function() {
		$("#btnAtualizarPerfil").attr('disabled', false);
	});	
}