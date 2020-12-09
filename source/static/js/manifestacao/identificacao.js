$(document).ready(function() {
	actionButtonRadioIdentificacao();
	modalLoginCidadao();
	actionButtonsCadastro();
	actionButtonContinuar();
	
	reloadInformacoes();
	
	onChangeTipoDocumento();
	focusOutDataNascimentoFuture();
	blockCopyCutPasteConfirmPasswordAndEmail();
	initializeSelectizeIdentificacao();
});

function actionButtonContinuar() {
	$("#btnContinuarFirstStep").click(function() {
		var is_identificacao = $("input[name='0-is_identificacao']").is(":checked");
		var is_not_identificacao = $("input[name='0-is_not_identificacao']").is(":checked");
		var has_not_cadastro = $("input[name='0-has_not_cadastro']").is(":checked");
		var is_ok = new Boolean('true');
		var id_usuario = $("#userId").val();
		var is_manifestacao_presencial = $("#is_manifestacao_presencial").val().toLowerCase() == 'true';
		
		if(is_manifestacao_presencial) {
			$("input[name='0-is_presencial']").prop('checked', true);
		} else {
			$("input[name='0-is_presencial']").prop('checked', false);
		}
		
		if (!is_manifestacao_presencial && !is_not_identificacao && !is_identificacao) {
			toastr.error('É preciso selecionar uma das opções de identificação.', 'Opção de identificação');
			is_ok = false;
		}
		
		if(is_identificacao) {
			if(!has_not_cadastro && !is_manifestacao_presencial && isNull(id_usuario)) {
				toastr.error('É preciso selecionar uma das opções de identificação.', 'Opção de identificação');
				is_ok = false;
			} 
			
			if(!is_manifestacao_presencial && !has_not_cadastro && isNull(id_usuario)) {
				toastr.error('Ao marcar que possui cadastro é obrigatório efetuar login. Clique em tenho cadastro para fazer login.', 'Opção de cadastro');
				is_ok = false;
			}
			
			if(is_manifestacao_presencial && !has_not_cadastro) {
				if(isNull($("#id_0-email_cidadao").val())) {
					toastr.error('É obrigatório informar o e-mail para consultar.', 'E-mail Cidadão');
					is_ok = false;
				} 
			}
		}
		
		if(is_ok) {
			if(is_not_identificacao) {
				$('input[type="email"]').val('');
				$('input[type="password"]').val('');
			}
			
			$("#formIdentificacao").submit();
		}
	});
}

function initializeSelectizeIdentificacao() {
	$('select').selectize({
		maxItems: 1, 
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		placeholder: 'Selecione...',
		selectOnTab: true,
	});
}

function reloadInformacoes() {
	var is_identificacao = $("input[name='0-is_identificacao']").is(":checked");
	var is_not_identificacao = $("input[name='0-is_not_identificacao']").is(":checked");
	var has_not_cadastro = $("input[name='0-has_not_cadastro']").is(":checked");
	var id_usuario_cidadao = $("#userId").val();
	var is_manifestacao_presencial = $("#is_manifestacao_presencial").val().toLowerCase() == 'true'; 
		
	if(is_manifestacao_presencial) {
		$("input[name='0-is_presencial']").prop('checked', true);
	} else {
		$("input[name='0-is_presencial']").prop('checked', false);
	}
	
	if(!isNull(id_usuario_cidadao)) {
		$("#btnQueroIdentificacoComAcesso").trigger('click');
		$("#btnContinuarFirstStep").trigger('click');
	} else {
		
		if(is_not_identificacao) {
			$("#btnNaoQueroIdentificacao").trigger('click');
		}
		
		if(is_identificacao) {
			$("#btnQueroIdentificacoComAcesso").trigger('click');
			
			if (has_not_cadastro) {
				$("#btnNaoPossuoCadastro").trigger('click');
			} else {
				if(is_manifestacao_presencial) {
					$("#btnPossuoCadastro").trigger('click');
				}
			}
		}
	}
}

function actionButtonRadioIdentificacao() {
	$("#btnQueroIdentificacoComAcesso").click(function() {
		$('.div-identificacao').find('.card').addClass('not-selected');
		$(this).parents('.card').removeClass('not-selected');
		var id_usuario = $("#userId").val();
		$('.div-btn-continuar').removeClass('d-none');
		$('label').removeClass('active');
		$(this).addClass('active');
		$("#divFormCidadao").addClass('d-none');
		
		if(isNull(id_usuario)) {
			$("#divButtonsCadastro").removeClass('d-none');
		}
		
		$("input[name='0-is_identificacao']").prop('checked', true);
		$("input[name='0-is_not_identificacao']").prop('checked', false);
		
		$('.card').removeClass('border-warning');
		$('.card').removeClass('border-danger');
		$(this).parents('.card').addClass('border-success');
		
		$('body').animate({
			scrollTop : $("#divButtonsCadastro").offset().top
		}, 1000);
	});
	
	$("#btnNaoQueroIdentificacao").click(function() {
		$("#divBuscarEmailCidadao").addClass('d-none');
		$('.div-identificacao').find('.card').addClass('not-selected');
		$(this).parents('.card').removeClass('not-selected');
		$('.div-btn-continuar').removeClass('d-none');
		$('label').removeClass('active');
		$(this).addClass('active');
		
		$('.card').removeClass('border-success');
		$('.card').removeClass('border-warning');
		$(this).parents('.card').addClass('border-danger');
		
		$("#divFormCidadao").addClass('d-none');
		$("#divButtonsCadastro").addClass('d-none');
		
		$("input[name='0-is_identificacao']").prop('checked', false);
		$("input[name='0-has_not_cadastro']").prop('checked', false);
		
		$("input[name='0-is_not_identificacao']").prop('checked', true);
	});
}

function actionButtonsCadastro() {
	$("#btnPossuoCadastro").click(function() {
		
		var is_manifestacao_presencial = $("#is_manifestacao_presencial").val().toLowerCase() == 'true';
		if(is_manifestacao_presencial) {
			$("#divBuscarEmailCidadao").removeClass('d-none');
		} else {
			$("#divBuscarEmailCidadao").addClass('d-none');
		} 
		$('.card-tenho-cadastro').removeClass('not-selected');
		$('#btnNaoPossuoCadastro').removeClass('active');
		$("#divFormCidadao").addClass('d-none');
		
		$(this).parents('.card').addClass('border-primary');
		$('.card-nao-tenho-cadastro').removeClass('border-danger');
		$('.card-nao-tenho-cadastro').addClass('not-selected');
		$("input[name='0-has_cadastro']").prop('checked', true);
		$("input[name='0-has_not_cadastro']").prop('checked', false);
	});
	
	$("#btnNaoPossuoCadastro").click(function() {
		$('.card-nao-tenho-cadastro').removeClass('not-selected');	
		$(this).addClass('active');
		$('#btnPossuoCadastro').removeClass('active');
		$("#divBuscarEmailCidadao").addClass('d-none');
		$("#divFormCidadao").removeClass('d-none');
		$(this).parents('.card').addClass('border-danger');
		$('.card-tenho-cadastro').removeClass('border-primary');
		$('.card-tenho-cadastro').addClass('not-selected');
		
		$("input[name='0-has_not_cadastro']").prop('checked', true);
		$("input[name='0-has_cadastro']").prop('checked', false);
		initializeSelectize();
		
		$('body').animate({
			scrollTop : $("#divDadosObrigatorios").offset().top
		}, 1000);
	});
}

function modalLoginCidadao() {
  	$('#modalWindow').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget);
		var tituloModal = 'Login do Cidadão';
		var modal = $(this);
		
		 var loading = $("#loading").clone();
			 loading.removeAttr("id");
			 loading.removeClass('d-none');
			 loading.find('#textoLoading').text('Carregando...');
			 loading.find('i').addClass('fa-10x').removeClass('fa-5x');
		
			modal.find('.modal-title').addClass('float-center')
			modal.find('.modal-title').text(tituloModal);
			modal.find('.modal-body').html($('<div class="text-center div-loading"/>').append(loading));
			modal.find('.modal-footer').addClass('d-none');
			
			$("<div class='div-identificacao'/>").load(button.data('href'), function() {
				modal.find('.modal-body').html($(this));
			});
			
	}).on('hide.bs.modal', function (e) {
		$(this).find('.modal-title').text('');
		
		var id_usuario = $("#userId").val();
		
		if(!isNull(id_usuario)) {
			$("#formIdentificacao").submit();
		}
	});
}

function blockCopyCutPasteConfirmPasswordAndEmail() {
	 $('#id_0-email, #id_0-email_confirm, #id_0-password ,#id_0-password_confirm').bind("cut copy paste",function(e) {
	     e.preventDefault();
	 });
}

function initializeSelectize() {
	$('.selectize').selectize({
		maxItems: 1,
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		placeholder: 'Selecione...',
		selectOnTab: true,
	});
}

function onChangeTipoDocumento() {
	$("#id_0-tipo_documento").change(function (){
		var valor = $(this).val();
		
		if(valor == 'CPF') {
			$("#id_0-tipo_documento_numero").mask('999.999.999-99');
		} else {
			$("#id_0-tipo_documento_numero").unmask();
		}
	});
}

function focusOutDataNascimentoFuture() {
	$('.data-nascimento').focusout(function() {
		var dataAtual = moment().format('YYYY-MM-DD');
		if(!isNull($(this).val())) {
			var selected  = moment($(this).val(), 'DD/MM/YYYY').format('YYYY-MM-DD');
			if(!isNull(selected) && selected > dataAtual) {
				$(this).addClass('is-invalid');
				toastr.error('A data de nascimento não pode ser uma data futura','Data de Nascimento');
			} else if($(this).hasClass('is-invalid')) {
				$(this).removeClass('is-invalid');
			}
		}
	});
}