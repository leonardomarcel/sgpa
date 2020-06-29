$(document).ready(function() {
	initializeSelectize();
	inicializarInputArquivo();
	$(".fileinput-remove ").removeClass("btn-secondary").addClass('btn-outline-danger');
	
	checkIfManifestacaoPresencial();
	
	formDoneManifestacao();
});
	

function formDoneManifestacao() {
	$("#formDoneManifestacao").submit(function() {
		// submit more than once return false
		$(this).submit(function() {
			return false;
		});
		// submit once return true
		$("#btnEnviarManifestacao").attr('disabled', true)
		$("#btnEnviarManifestacao").find('span').text('Enviando...')
		return true;
	});
}

function checkIfManifestacaoPresencial() {
	var is_manifestacao_presencial = $("#is_manifestacao_presencial").val().toLowerCase() == 'true'; 
	
	if(is_manifestacao_presencial) {
		$("input[name='2-is_presencial']").prop('checked', true);
	} else {
		$("input[name='2-is_presencial']").prop('checked', false);
	}
}

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
	
function inicializarInputArquivo() {
	$("input[type='file']").fileinput({
		language: "pt-BR",
        maxFilePreviewSize: 10240,
        showUpload: false,
        maxFileSize: 10240,
        multiple: true,
        maxFilesNum : 10,
        allowedFileExtensions: ["jpeg","jpg", "png", "gif", "pdf"],
        msgInvalidFileExtension: 'Extensão inválida para o arquivo "<b>{name}</b>". Apenas arquivos com extensões "[<b>{extensions}</b>]" são permitidos.',
        msgSizeTooLarge: 'O arquivo <b>{name}</b> (<b>{size} KB</b>) excede o tamanho máximo permitido de <b>{maxSize} KB</b>.',
        
        fileSizeGetter: function (bytes) {
            var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024))),
                sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
            var resultado = (bytes / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + sizes[i];
            return resultado;
        },
    });
	$(".fileinput-upload-button").addClass('d-none');
	$(".fileinput-remove ").removeClass("btn-secondary").addClass('btn-outline-danger');
}