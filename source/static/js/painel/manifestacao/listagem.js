var $selectizeAssunto;

$(document).ready(function() {
	$('#id_numero_protocolo').mask('99999/9999');
	$('[data-toggle="tooltip"]').tooltip();
	initializeSelectize();
	
	$selectizeAssunto = $("#id_assunto")[0].selectize;
	$selectizeAssunto.disable();
	
	onChangeTipoAssunto();
	onClickAccordionDetalhes();
	actionButtonFiltroCompleto();
	
	verifyParametersAndShowCollapse();
	onChangeTipoEntrada();
	
	$('[data-toggle=popover]').popover({
		trigger: 'hover',
		placement: 'top',
		html: true
	});
});

function clearOptionsTipoPresencial() {
	var $select = $('#id_tipo_presencial').selectize();
	var control = $select[0].selectize;
	control.clear();
}

function onChangeTipoEntrada() {
	if($("#id_tipo_entrada").val() == 'P') {
		$("#divTipoPresencial").removeClass('d-none');
	} else {
		$("#divTipoPresencial").addClass('d-none');
		clearOptionsTipoPresencial();
	}
	
	
	$("#id_tipo_entrada").change(function () {
		var tipo = $(this).val();
		
		if(tipo == 'P') {
			$("#divTipoPresencial").removeClass('d-none');
		} else {
			$("#divTipoPresencial").addClass('d-none');
			clearOptionsTipoPresencial();
		}
	})
}

function initializeSelectize() {
	$('#id_assunto').selectize({
		maxItems: 1,
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		placeholder: '--- ESCOLHA UM TIPO DE ASSUNTO ---',
		selectOnTab: true,
	});
	
	$('select').selectize({
		maxItems: 1,
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		placeholder: '--- TODOS ---',
		selectOnTab: true,
	});
}

function onChangeTipoAssunto() {
	$("#id_tipo_assunto").change(function () {
		var id_tipo_assunto = $(this).val();
		
		if(id_tipo_assunto != null) {
			$selectizeAssunto.enable();
			$selectizeAssunto.clearOptions();
			$selectizeAssunto.load(function(callback) {
	    		$.getJSON('/publico/assuntos_json/'+ id_tipo_assunto, function(data) {
					 callback(data);
				}).fail(function() {
					if(!isNull(id_tipo_assunto)) {
						toastr.error('Ocorreu um problema ao tentar carregar os assuntos.', 'Assuntos');
					}
				}).done(function() {
					$selectizeAssunto.enable();
				});
	    	});
		}
	});
}

function onClickAccordionDetalhes() {
	$('.click-detalhes').click(function() {
		var id = $(this).data('id');
		if($(".detalhes[data-id='"+ id +"']").hasClass('hide')) {
			$(".detalhes[data-id='"+ id +"']").removeClass('hide');
		} else {
			$(".detalhes[data-id='"+ id +"']").addClass('hide');
		}
	});
}

function actionButtonFiltroCompleto() {
	$(".btn-filtro-completo").click(function() {
		if($(this).hasClass('active')) {
			$(this).removeClass('active');
			$(this).find('i').removeClass('fa-eye-slash').addClass('fa-eye');
		} else {
			$(this).addClass('active');
			$(this).find('i').removeClass('fa-eye').addClass('fa-eye-slash');
		}
	});
}

function verifyParametersAndShowCollapse() {
	$.urlParam = function(name){
	    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
	    if (results==null){
	       return null;
	    }
	    else{
	       return decodeURI(results[1]) || 0;
	    }
	}
	
	var has_data_inicio = !isNull($.urlParam('data_inicio')) && $.urlParam('data_inicio') != 0;
	var has_data_termino = !isNull($.urlParam('data_termino')) && $.urlParam('data_termino') != 0;
	var has_ouvidoria_origem = !isNull($.urlParam('ouvidoria_origem')) && $.urlParam('ouvidoria_origem') != 0;
	var has_ouvidoria_destino = !isNull($.urlParam('ouvidoria_destino')) && $.urlParam('ouvidoria_destino') != 0;
	var has_identificacao = !isNull($.urlParam('identificacao')) && $.urlParam('identificacao') != 'T';
	var has_gestor = !isNull($.urlParam('gestor')) && $.urlParam('gestor') != 0;
	if(has_data_inicio || has_data_termino || has_ouvidoria_origem || has_ouvidoria_destino || has_identificacao || has_gestor) {
		$(".btn-filtro-completo").trigger('click');
	}
}