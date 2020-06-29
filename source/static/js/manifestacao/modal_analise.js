$(document).ready(function() {
	initializeSelectize();	
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