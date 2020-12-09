$(document).ready(function() {
	initializeSelectize();
	$('[data-toggle="tooltip"]').tooltip();
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