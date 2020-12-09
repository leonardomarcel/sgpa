var titulo_alteracao = 'Confirmação';
var $selectizeAssunto;
var idIsPermissaoAvaliar;
var has_exists_prazo_prorrogado;

$(document).ready(function() {
	initializeSelectize();
	
	loadBindsBotoesEditar();
	loadActions();
	actionButtonRemoverAnexo();
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

function loadBindsBotoesEditar() {
	$('.btn-acoes').unbind("click");
	actionButtonArquivarManifestacao();
	actionButtonEditarInserirResposta();
	actionButtonInserirResposta();
	actionButtonEditarOuvidoriaDestino();
	actionButtonEditarTipoManifestacao();
	actionButtonEditarAssunto();
	actionButtonReabrirManifestacao();
	actionButtonProrrogarPrazo();
	actionButtonRespostaConclusiva();
	actionButtonRespostaIntermediaria();
	actionButtonEditarAnexos();
	actionButtonEditarComplementacao();
	inicializarInputArquivo();
	actionButtonEnviarPedidoComplementacao();
	idIsPermissaoAvaliar = $.trim($("#idIsPermissaoAvaliar").val()).toUpperCase()  == 'TRUE';
	has_exists_prazo_prorrogado = $.trim($("#has_exists_prazo_prorrogado").val()).toUpperCase()  == 'TRUE';
}

function onChangeSelectGestor() {
	$("#id_gestor").change(function() {
		var idGestorAtual = $("#idGestorResponsavel").val();
		var idSelecionado = $(this).val();

		if (idGestorAtual != idSelecionado && idIsPermissaoAvaliar) {
			$('#btnTransferirResponsavel').prop("disabled", false);
		} else {
			$('#btnTransferirResponsavel').prop("disabled", true);
		}
	});
}

function onChangeSelectAssunto() {
	$("#id_assunto").change(function() {
		var idAssuntoAtual = $("#idAssuntoHidden").val();
		var idSelecionado = $(this).val();

		if (idAssuntoAtual != idSelecionado) {
			$('#btnSalvarAssunto').prop("disabled", false);
		} else {
			$('#btnSalvarAssunto').prop("disabled", true);
		}
	});
}

function onChangeSelectTipoManifestacao() {
	$("#id_tipo_manifestacao").bind('change', function() {
		var tipoSolicitacaoAtual = $("#idTipoManifestacaoHidden").val();
		var tipoSolicitacaoSelecionada = $(this).val();

		if (tipoSolicitacaoAtual != tipoSolicitacaoSelecionada) {
			$('#btnSalvarTipoManifestacao').prop("disabled", false);
		} else {
			$('#btnSalvarTipoManifestacao').prop("disabled", true);
		}
	});
}

function actionButtonEditarComplementacao() {
	$("#btnComplementar").click(function(e) {
		$('.complementacao-form').removeClass('d-none');
		$("#btnCancelarComplementacao").removeClass('hide');
		actionButtonCancelarComplementacao();
		$('html, body').animate({
			scrollTop : $("#cardBodyComplementacao").offset().top
		}, 1000);
	});
}

function actionButtonEnviarPedidoComplementacao() {
	$("#btnEnviarComplementacao").click(function() {
		var idPedidoComplementacao = $("#id_complementacao").val();
		
		if(isNull(idPedidoComplementacao)) {
			toastr.error('É obrigatório informar o pedido de complementação.', 'Pedido de Complementação');
		} else {
			ajaxEnviarPedidoComplementacao();
		}
	});
}

function actionButtonCancelarComplementacao() {
	$("#btnCancelarComplementacao").click(function(e) {
		$('.complementacao-form').addClass('d-none');
		$(this).addClass('hide');
	});
}

function keyPressJustificativaCheckIfTexto() {
	$("#id_justificativa").bind('input propertychange', function() {
		if (this.value.length && hasChangeOuvidoriaDestino()) {
			$('#btnSalvarOuvidoriaDestino').prop("disabled", false);
		} else {
			$('#btnSalvarOuvidoriaDestino').prop("disabled", true);
		}
	});
}

function onChangeSelectOuvidoriaDestino() {
	$("#id_ouvidoria_destino").bind('change', function() {
		var ouvidoriaAtual = $("#idOuvidoriaDestinoHidden").val();
		var ouvidoriaSelecionado = $(this).val();
		var justificativa = $("#id_justificativa").val();
		
		if (hasChangeOuvidoriaDestino() && justificativa.length) {
			$('#btnSalvarOuvidoriaDestino').prop("disabled", false);
		} else {
			$('#btnSalvarOuvidoriaDestino').prop("disabled", true);
		}
	});
}

function hasChangeOuvidoriaDestino() {
	var idOuvidoriaDestinoHidden = $("#idOuvidoriaDestinoHidden").val();
	var idOuvidoriaDestinoSelecionado = $("#id_ouvidoria_destino").val();
	return idOuvidoriaDestinoHidden != idOuvidoriaDestinoSelecionado;
}

function actionButtonInserirResposta() {
	$("#labelRespostaConclusiva").bind('click', function() {
		$("input[name='is_resposta']").prop('checked', true);
		$("#divResposta").removeClass('d-none');
	});
}

function actionButtonEditarAnexos() {
	$("#btnEditarAnexos").bind('click', function(e) {
		$(".card-body-inserir-anexos").removeClass('d-none');
		$(".card-body-inserir-anexos").removeClass('card-body-no-padding');
		inicializarInputArquivo();
		
		$('html, body').animate({
			scrollTop : $(".card-body-inserir-anexos").offset().top
		}, 1000);
	});
}

function actionButtonEditarInserirResposta() {
	$("#btnEditarInserirResposta").bind('click', function(e) {
		$('#cardInserirResposta').removeClass('d-none');
		$("#btnCancelarInserirResposta").removeClass('hide');
		
		if($("#cardBodyInserirResposta").hasClass('d-none')) {
			$("#cardBodyInserirResposta").removeClass('d-none');
		}
		
		actionButtonCancelarInserirResposta();
		$('html, body').animate({
			scrollTop : $(".card-resposta-conclusiva").offset().top
		}, 1000);
	});
}

function actionButtonRespostaIntermediaria() {
	$("#btnRespostaIntermediaria").bind('click', function() {
		$('.card-resposta-conclusiva').addClass('not-selected');
		$('label').removeClass('active');
		$(this).parents('.card').removeClass('not-selected');
		$(this).addClass('active');
		$('.div-texto-resposta').removeClass('d-none');
		$('.div-btn-salvar-inserir-resposta').removeClass('d-none');

		$("input[name='is_resposta_intermediaria']").prop('checked', true);
		$("input[name='is_resposta_conclusiva']").prop('checked', false);
		$("#btnSalvarInserirResposta").find('span').text(' Salvar resposta intermediária');
	});
}

function actionButtonRespostaConclusiva() {
	$("#btnRespostaConclusiva").bind('click', function() {
		$('.card-resposta-intermediaria').addClass('not-selected');
		$('label').removeClass('active');
		$(this).parents('.card').removeClass('not-selected');
		$(this).addClass('active');

		$('.div-btn-salvar-inserir-resposta').removeClass('d-none');
		$('.div-texto-resposta').removeClass('d-none');
		$("input[name='is_resposta_conclusiva']").prop('checked', true);
		$("input[name='is_resposta_intermediaria']").prop('checked', false);
		$("#btnSalvarInserirResposta").find('span').text(' Salvar resposta conclusiva');
	});
}

function actionButtonEditarAssunto() {
	$("#btnEditarAssunto").bind('click', function(e) {
		$('.assunto-form').removeClass('d-none');
		$("#btnCancelarAssunto").removeClass('hide');
		actionButtonCancelarAssunto();
		$('html, body').animate({
			scrollTop : $("#cardBodyAssunto").offset().top
		}, 1000);
	});
}

function actionButtonEditarOuvidoriaDestino() {
	$("#btnEditarOuvidoriaDestino").click(function(e) {
		$('.ouvidoria-destino-form').removeClass('d-none');
		$("#btnCancelarOuvidoriaDestino").removeClass('hide');
		actionButtonCancelarOuvidoriaDestino();
		$('html, body').animate({
			scrollTop : $("#cardBodyOuvidoriaDestino").offset().top
		}, 1000);
	});
}

function actionButtonCancelarOuvidoriaDestino() {
	$("#btnCancelarOuvidoriaDestino").click(function(e) {
		$('.ouvidoria-destino-form').addClass('d-none');
		$(this).addClass('hide');
	});
}

function actionButtonEditarTipoManifestacao() {
	$("#btnEditarTipoManifestacao").click(function(e) {
		$('.tipo-manifestacao-form').removeClass('d-none');
		$("#btnCancelarTipoManifestacao").removeClass('hide');
		actionButtonCancelarTipoManifestacao();
		$('html, body').animate({
			scrollTop : $("#cardBodyTipoManifestacao").offset().top
		}, 1000);
	});
}

function actionButtonCancelarInserirResposta() {
	$("#btnCancelarInserirResposta").click(function(e) {
		$(this).addClass('hide');
	});
}

function actionButtonCancelarTipoManifestacao() {
	$("#btnCancelarTipoManifestacao").click(function(e) {
		$('.tipo-manifestacao-form').addClass('d-none');
		$(this).addClass('hide');
	});
}

function actionButtonCancelarAssunto() {
	$("#btnCancelarAssunto").click(function(e) {
		$('.assunto-form').addClass('d-none');
		$(this).addClass('hide');
	});
}

function actionButtonSalvarTipoManifestacao() {
	$("#btnSalvarTipoManifestacao").click(function() {
		var idTipoManifestacaoAtual = $("#idTipoManifestacaoHidden").val();
		var idTipoManifestacaoSelecionado = $("#id_tipo_manifestacao").val();

		if (idTipoManifestacaoAtual != idTipoManifestacaoSelecionado) {
			ajaxSalvarTipoManifestacao();
		}
	});
}

function changeColorPanelsByTipoManifestacao(idTipoManifestacaoAtual, idTipoManifestacaoSelecionado) {
	$(".card").removeClass('border-' + idTipoManifestacaoAtual).addClass('border-' + idTipoManifestacaoSelecionado);
	$(".card-header").removeClass('bg-' + idTipoManifestacaoAtual).addClass('bg-' + idTipoManifestacaoSelecionado);
}

function actionButtonSalvarOuvidoriaDestino() {
	$("#btnSalvarOuvidoriaDestino").click(function() {
		var justificativa = $("#id_justificativa").val();
		
		if(isNull(justificativa)) {
			toastr.error('É obrigatório informar a justificativa.', 'Encaminhar/Movimentar');
		}
		if (hasChangeOuvidoriaDestino() && !isNull(justificativa)) {
			ajaxSalvarOuvidoriaDestino();
		}
	});
}

function actionButtonSalvarAssunto() {
	$("#btnSalvarAssunto").click(function() {
		var idAssuntoAtual = $("#idAssuntoHidden").val();
		var idTipoAssuntoHidden = $("#idTipoAssuntoHidden").val();
		var idTipoAssuntoSelecionado = $("#id_tipo_assunto").val();
		var idAssuntoSelecionado = $("#id_assunto").val();
		
		if(isNull(idAssuntoSelecionado)) {
			toastr.error('É obrigatório informar o assunto.', 'Assunto');
		} else {
			if (idAssuntoAtual != idAssuntoSelecionado) {
				ajaxSalvarAssunto();
			}
		}
	});
}

function actionButtonSalvarInserirResposta() {
	$("#btnSalvarInserirResposta").click(function() {
		if($(".cke_editable p").innerHTML == "") {
			toastr.error('É obrigatório preencher a resposta.', 'Resposta');
		} else {
			var resposta = $("#id_resposta").val();
			if(isNull(resposta)) {
				toastr.error('É obrigatório preencher a resposta.', 'Resposta');
			} else {
				ajaxSalvarInserirResposta();
			}
		}
	});
}

function onChangeRespostaConclusiva() {
	$("#is_resposta_conclusiva").click(function() {
		if ($(this).is(':checked')) {
			$("#divMensagemRespostaConclusiva").removeClass('d-none');
			$("#btnSalvarDadosManifestacao").prop("disabled", false);
		} else {
			$("#divMensagemRespostaConclusiva").addClass('d-none');
		}
	});
}

function ajaxAlterarResponsavel() {
	$.ajax({
		url : '/painel/manifestacao/alterar_responsavel/',
		type : 'POST',
		data : $("#formAlterarResponsavel").serialize(),

		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar alterar o responsável da manifestação.", 'Responsável');
		},

		beforeSend : function() {
			showLoading('cardBodyResponsavel');
		},

		success : function(data) {
			toastr.success("O responsável da manifestação foi alterado com sucesso.", 'Responsável');
			$("#cardBodyResponsavel").html(data);
		},

		complete : function() {
			loadMovimentacoes();
		}
	});
}

function onChangeManifestacaoInformacaoPessoal() {
	if ($("#has_informacao_pessoal").is(':checked')) {
		$("#has_informacao_pessoal").prop('checked', false);
	} else {
		$("#has_informacao_pessoal").prop('checked', true);
	}
}

function confirmAlterarResponsavel() {
	$("#btnTransferirResponsavel").click(function(e) {
		bootbox.confirm({
			title : titulo_alteracao,
			message : "Tem certeza que deseja alterar o responsável para essa manifestação ?",
			size : 'medium',
			buttons : {
				confirm : {
					label : 'Confirmar',
					className : 'btn-success outline'
				},

				cancel : {
					label : 'Cancelar',
					className : 'btn-danger outline'
				}
			},

			callback : function(result) {
				if (result) {
					ajaxAlterarResponsavel();
				}
			}
		});
	});
}

function confirmManifestacaoInformacaoPessoal() {
	$("#has_informacao_pessoal").click(function(e) {

		bootbox.confirm({
			title : titulo_alteracao,
			message : "Tem certeza que deseja arquivar essa manifestação ?",
			size : 'medium',
			buttons : {
				confirm : {
					label : 'Confirmar',
					className : 'btn-success outline'
				},

				cancel : {
					label : 'Cancelar',
					className : 'btn-danger outline'
				}
			},

			callback : function(result) {
				if (result) {
					ajaxManifestacaoInformacaoPessoal();
				}
			}
		});
	});
}

function confirmManifestacaoInformacaoPessoal() {
	$("#has_informacao_pessoal").click(function(e) {
		if (!idIsPermissaoAvaliar) {
			toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
		} else {
		e.preventDefault();
		var mensagem = "";

		if ($(this).is(':checked')) {
			mensagem = "O Contéudo da manifestação não poderá ser publicado.";
		} else {
			mensagem = "O Contéudo da manifestação poderá ser publicado.";
		}
			bootbox.confirm({
				title : titulo_alteracao,
				message : mensagem,
				size : 'medium',
				buttons : {
					confirm : {
						label : 'Confirmar',
						className : 'btn-success outline'
					},
	
					cancel : {
						label : 'Cancelar',
						className : 'btn-danger outline'
					}
				},
	
				callback : function(result) {
					if (result) {
						onChangeManifestacaoInformacaoPessoal();
						ajaxManifestacaoInformacaoPessoal();
					}
				}
			});
		}
	});
}

function confirmAnalisarManifestacao() {
	$("#btnAnalisarManifestacao").click(function() {
		if (!idIsPermissaoAvaliar) {
			toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
		} else {
			
			bootbox.confirm({
				title : 'Confirmação da Análise',
				message : 'Tem certeza que deseja analisar essa manifestação ?',
				size : 'medium',
				buttons : {
					confirm : {
						label : 'Confirmar',
						className : 'btn-success outline'
					},
	
					cancel : {
						label : 'Cancelar',
						className : 'btn-danger outline'
					}
				},
	
				callback : function(result) {
					if (result) {
						ajaxAnalisarManifestacao();
					}
				}
			});
		}
	});
}

function ajaxAnalisarManifestacao() {
	var idManifestacao = $("#idManifestacaoHidden").val();

	$.ajax({
		url : '/painel/manifestacao/analisar_manifestacao/' + encodeURIComponent(idManifestacao),
		type : 'GET',

		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar analisar a manifestação.", 'Em análise');
		},

		beforeSend : function() {
			showLoading('divManifestacao');
		},

		success : function(data) {
			toastr.success("O status da manifestação foi modificado para em análise.", 'Em análise');
			$("#divAnaliseManifestacao").html(data);
		},

		complete : function() {
			window.location.reload();
		}
	});
}

var is_resposta;
function loadRespostasManifestacao() {
	var idManifestacao = $("#idManifestacaoHidden").val();
	$.ajax({
			url : '/painel/manifestacao/load_respostas_manifestacao/' + encodeURIComponent(idManifestacao),
			type : 'GET',

			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao buscar as respostas dessa manifestação.", "Respostas");
			},

			beforeSend : function() {
				showLoading('cardRespostasManifestacao');
				$('html, body').animate({ scrollTop : $("#cardRespostasManifestacao").offset().top }, 1000);
			},

			success : function(data) {
				$("#cardBodyRespostasManifestacao").html(data);
			},

			complete : function() {
				loadMovimentacoes();
			}
		});
}

function actionButtonProrrogarPrazo() {
	$("#btnProrrogarPrazo").bind('click', function() {
		if (!idIsPermissaoAvaliar) {
			toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
		} else {
			
			if(has_exists_prazo_prorrogado) {
				toastr.error('Essa manifestação já foi prorrogada uma vez!', 'Manifestação Prorrogada');
			} else {
				
				bootbox.prompt({
					title : 'Justificativa para prorrogar prazo',
					message : "Tem certeza que deseja prorrogar essa manifestação ?",
					inputType : 'textarea',
					size : 'medium',
					buttons : {
						confirm : {
							label : 'Confirmar',
							className : 'btn-success outline'
						},
	
						cancel : {
							label : 'Cancelar',
							className : 'btn-danger outline'
						}
					},
	
					callback : function(result) { 
						if (result != null) {
							var justificativa = $(this).find(".bootbox-form textarea").val();
	
							if (isNull(justificativa)) {
								toastr.error('É obrigatório preencher a justificativa');
								$(".bootbox-form textarea").addClass('is-invalid');
								$(".bootbox-form textarea").focus();
								return false;
							} else {
								ajaxProrrogarManifestacao(justificativa);
							}
						}
					}
				});
			}
		}
	});
}

function actionButtonArquivarManifestacao() {
	$("#btnArquivarManifestacao").bind('click', function() {
		if (!idIsPermissaoAvaliar) {
			toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
		} else {
			bootbox.prompt({
				title : 'Justificativa do arquivamento',
				message : "Tem certeza que deseja arquivar essa manifestação ?",
				inputType : 'textarea',
				size : 'medium',
				buttons : {
					confirm : {
						label : 'Confirmar',
						className : 'btn-success outline'
					},

					cancel : {
						label : 'Cancelar',
						className : 'btn-danger outline'
					}
				},

				callback : function(result) {
					if (result != null) {
						var justificativa = $(this).find(".bootbox-form textarea").val();

						if (isNull(justificativa)) {
							toastr.error('É obrigatório preencher a justificativa');
							$(".bootbox-form textarea").addClass('is-invalid');
							$(".bootbox-form textarea").focus();
							return false;
						} else {
							ajaxArquivarManifestacao(justificativa);
						}
					}
				}
			});
		}
	});
}

function actionButtonReabrirManifestacao() {
	$("#btnReabrirManifestacao").bind('click', function() {
		if (!idIsPermissaoAvaliar) {
			toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
		} else {
			bootbox.prompt({
				title : 'Justificativa da Reabertura',
				message : "Tem certeza que deseja reabrir essa manifestação ?",
				inputType : 'textarea',
				size : 'medium',
				buttons : {
					confirm : {
						label : 'Confirmar',
						className : 'btn-success outline'
					},

					cancel : {
						label : 'Cancelar',
						className : 'btn-danger outline'
					}
				},

				callback : function(result) {
					if (result != null) {
						var justificativa = $(this).find(".bootbox-form textarea").val();

						if (isNull(justificativa)) {
							toastr.error('É obrigatório preencher a justificativa');
							$(".bootbox-form textarea").addClass('is-invalid');
							$(".bootbox-form textarea").focus();
							return false;
						} else {
							ajaxReabrirManifestacao(justificativa);
						}
					}
				}
			});
		}
	});
}

function ajaxReabrirManifestacao(justificativa_value) {
	var $formAjaxManifestacao = $("#formAjaxManifestacao").clone();
	var $justificativa = createInputHidden('justificativa', 'justificativa', justificativa_value);
	$formAjaxManifestacao.append($justificativa);
	
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		$.ajax({
			url : '/painel/manifestacao/reabrir_manifestacao/',
			type : 'POST',
			data : $formAjaxManifestacao.serialize(),
	
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar arquivar essa manifestação.", 'Manifestação Reaberta');
			},
	
			beforeSend : function() {
				showLoading('cardBodyManifestacao');
			},
	
			success : function(data) {
				$("#cardBodyManifestacao").html(data);
				toastr.success("A manifestação foi reaberta com sucesso.", 'Manifestação Reaberta');
				window.location.reload();
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function ajaxProrrogarManifestacao(justificativa_value) {
	var $formAjaxManifestacao = $("#formAjaxManifestacao").clone();
	var $justificativa = createInputHidden('justificativa', 'justificativa', justificativa_value);
	$formAjaxManifestacao.append($justificativa);
	
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		$.ajax({
				url : '/painel/manifestacao/prorrogar_prazo_manifestacao/',
				type : 'POST',
				data : $formAjaxManifestacao.serialize(),

				error : function(a, b, c) {
					toastr.error("Ocorreu um problema ao tentar prorrogar o prazo dessa manifestação.", 'Prorrogar Prazo');
				},

				beforeSend : function() {
					showLoading('cardManifestacao');
				},

				success : function(data) {
					$("#cardBodyManifestacao").html(data);
					toastr.success("O prazo da manifestação foi prorrogado com sucesso.", 'Prorrogar Prazo');
				},

				complete : function() {
					loadMovimentacoes();
				}
			});
	}
}

function ajaxArquivarManifestacao(justificativa_value) {
	var $formAjaxManifestacao = $("#formAjaxManifestacao").clone();
	var $justificativa = createInputHidden('justificativa', 'justificativa', justificativa_value);
	$formAjaxManifestacao.append($justificativa);
	
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		$.ajax({
			url : '/painel/manifestacao/arquivar_manifestacao/',
			type : 'POST',
			data : $formAjaxManifestacao.serialize(),
	
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar arquivar essa manifestação.", 'Manifestação Arquivar');
			},
	
			beforeSend : function() {
				showLoading('cardTipoManifestacao');
			},
	
			success : function(data) {
				$("#cardBodyManifestacao").html(data);
				toastr.success("A manifestação foi arquivada com sucesso.", 'Manifestação Arquivar');
				window.location.reload();
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function ajaxManifestacaoInformacaoPessoal() {
	var idManifestacao = $("#idManifestacaoHidden").val();
	var flag_informacao_pessoal = $("#has_informacao_pessoal").is(':checked') ? 'S' : 'N';
	
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		$.ajax({
			url : '/painel/manifestacao/assinalar_informacao_pessoal/' + encodeURIComponent(idManifestacao) + '/' + flag_informacao_pessoal,
			type : 'GET',
	
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar alterar a informação pessoal da manifestação.", 'Informação Pessoal');
			},
	
			success : function(data) {
				toastr.success("A manifestação foi alterada com sucesso.", 'Informação pessoal');
				$("#cardBodyManifestacao").html(data);
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function actionButtonRefreshMovimentacoes() {
	$(".btn-refresh-movimentacoes").click(function() {
		loadMovimentacoes();
	});
}

function loadManifestacao() {
	var idManifestacao = $("#idManifestacaoHidden").val();
	$.ajax({
		url : '/painel/manifestacao/load_manifestacao/' + encodeURIComponent(idManifestacao),
		type : 'GET',

		beforeSend : function() {
			showLoading('cardManifestacao');
		},

		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao buscar os dados da manifestação.", 'Dados Manifestação');
		},

		success : function(data) {
			$("#cardBodyManifestacao").html(data);
		},

		complete : function() {
			loadMovimentacoes();
		}
	});
}

function loadMovimentacoes() {
	var idManifestacao = $("#idManifestacaoHidden").val();
	$.ajax({
		url : '/painel/manifestacao/load_movimentacoes_manifestacao/' + encodeURIComponent(idManifestacao),
		type : 'GET',

		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao buscar as movimentações da manifestação.", 'Timeline Manifestação');
		},

		beforeSend : function() {
			showLoading('cardTimeline');
		},

		success : function(data) {
			$("#cardBodyTimeline").html(data);
		},

		complete : function() {
			loadActions();
			$('[data-toggle=popover]').popover({
				trigger: 'hover',
				placement: 'top',
				html: true
			});
		}
	});
}

function loadActions() {
	initializeSelectize();
	
	$selectizeAssunto = $("#id_assunto")[0].selectize;
	
	$('#id_numero_protocolo').mask('99999/9999');
	$('[data-toggle="tooltip"]').tooltip();
	
	$('[data-toggle=popover]').popover({
		trigger: 'hover',
		placement: 'top',
		html: true
	});
	
	onChangeTipoAssunto();
	onChangeSelectAssunto();
	onChangeSelectTipoManifestacao();
	onChangeSelectOuvidoriaDestino();
	onChangeRespostaConclusiva();

	actionButtonSalvarAssunto();
	actionButtonSalvarTipoManifestacao();
	actionButtonSalvarInserirResposta();
	actionButtonSalvarOuvidoriaDestino();

	actionButtonRefreshMovimentacoes();

	keyPressJustificativaCheckIfTexto();
	confirmAnalisarManifestacao();
	confirmManifestacaoInformacaoPessoal();
	onChangeSelectGestor();
	confirmAlterarResponsavel();
	
	$.each($('.btn-cancelar'), function() {
		if (!$(this).hasClass('hide')) {
			$(this).addClass('hide');
		}
	});
}

var idTipoManifestacaoAtual;
var idTipoManifestacaoSelecionado;

function ajaxSalvarTipoManifestacao() {
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
	
		$.ajax({
			url : '/painel/manifestacao/alterar_tipo_manifestacao/',
			type : 'POST',
			data : $("#formTipoManifestacao").serialize(),
	
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar alterar o tipo da manifestação.", 'Tipo de Manifestação');
			},
	
			beforeSend : function() {
				idTipoManifestacaoAtual = $("#idTipoManifestacaoHidden").val();
				idTipoManifestacaoSelecionado = $("#id_tipo_manifestacao").val();
				showLoading('cardTipoManifestacao');
			},
	
			success : function(data) {
				toastr.success("O tipo de manifestação foi alterado com sucesso.", 'Tipo de Manifestação');
				$("#cardBodyTipoManifestacao").html(data);
				changeColorPanelsByTipoManifestacao(idTipoManifestacaoAtual, idTipoManifestacaoSelecionado);
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function ajaxSalvarOuvidoriaDestino() {
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		$.ajax({
			url : '/painel/manifestacao/transferir_manifestacao/',
			type : 'POST',
			data : $("#formOuvidoriaDestino").serialize(),
	
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar transferir a manifestação.", 'Transferência de Ouvidoria');
			},
	
			beforeSend : function() {
				showLoading('cardOuvidoriaDestino');
			},
	
			success : function(data) {
				toastr.success("A manifestação foi transferida com sucesso.", 'Movimentação de Ouvidoria');
				$("#cardBodyOuvidoriaDestino").html(data);
				window.location.reload();
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function ajaxSalvarAssunto() {
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		$.ajax({
			url : '/painel/manifestacao/alterar_assunto/',
			type : 'POST',
			data : $("#formAssunto").serialize(),
	
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar alterar o assunto da manifestação.", 'Assunto');
			},
	
			beforeSend : function() {
				showLoading('cardAssunto', 'Salvando');
			},
	
			success : function(data) {
				toastr.success("O assunto foi alterado com sucesso.", 'Assunto');
				$("#cardBodyAssunto").html(data);
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function updateCkEditorAllMessageForms() {
    for(instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
}

function ajaxSalvarInserirResposta() {
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
		//updateCkEditorAllMessageForms();
		$.ajax({
			url : '/painel/manifestacao/inserir_resposta/',
			type : 'POST',
			data : $("#formInserirResposta").serialize(),
	
			beforeSend : function() {
				is_resposta = $("input[name='is_resposta_conclusiva']").is(':checked');
				showLoading('cardInserirResposta');
			},
	
			error : function(error, b, c) {
				if(error) {
					toastr.error(error.responseText, 'Resposta')
				} else {
					toastr.error("Ocorreu um problema ao tentar inserir a resposta para a manifestação.", 'Resposta')
				}
			},
	
			success : function(data) {
				if(is_resposta) {
					toastr.success("Resposta conclusiva salva com sucesso. A manifestação foi encerrada. ", 'Resposta Conclusiva');
				} else {
					toastr.success("Resposta intermediária salva com sucesso.", 'Resposta Intermediária');
				}
				
				$("#cardBodyInserirResposta").html(data);
				
				if (is_resposta) {
					window.location.reload();
				}
			},
	
			complete : function() {
				window.location.reload();
			}
		});
	}
}

function actionEditarDadosManifestacao() {
	var idManifestacao = $("#idManifestacaoHidden").val();
}

function showLoading(id) {
	var loading = $("#loading").clone();
	loading.removeAttr("id");
	loading.removeClass('d-none');
	$("#" + id + " .card-body").html($('<div class="text-center mt-2 div-loading"/>').append(loading));
}

function createInputHidden(id, name, value) {
	return $('<input>').attr({
		type : 'hidden',
		id : id,
		name : name,
		value : value
	});
}

function createInputFile(id, name, value) {
	return $('<input>').attr({
		type : 'file',
		id : id,
		name : name,
		value : value
	});
}

var uploadID = 0;
var sequencial = 1;
var tamanhoMaximoKB = 10240;
var hasNotErrorSelectFile = true;
var mensagemDeErro = "";
var totalArquivoComErro = 0;

function inicializarInputArquivo() {
	$("#id_files").fileinput({
		language: "pt-BR",
        maxFilePreviewSize: 10240,
        showUpload: false,
        uploadAsync : false,
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
}

function ajaxRemoverAnexo(id_arquivo) {
	if (!idIsPermissaoAvaliar) {
		toastr.error('Você não possui permissão para avaliar essa manifestação', 'Permissão Negada');
	} else {
	
		var $formAjaxManifestacao = $("#formAjaxManifestacao").clone();
		var $arquivo = createInputHidden('id_arquivo', 'id_arquivo', id_arquivo);
		$formAjaxManifestacao.append($arquivo);
		
		$.ajax({
			type: "POST",
			url: '/painel/manifestacao/remover_anexo/',
			data: $formAjaxManifestacao.serialize(),
			
			error : function(a, b, c) {
				toastr.error("Ocorreu um problema ao tentar apagar esse arquivo.", 'Remover Anexo da Manifestação');
			},
	
			beforeSend : function() {
				showLoading('tableAnexos');
			},
	
			success : function(data) {
				$("#tableAnexos").html(data);
				toastr.success("Os anexos foram enviados com sucesso.", 'Anexo da Manifestação');
				actionButtonRemoverAnexo();
			},
	
			complete : function() {
				loadMovimentacoes();
			}
		});
	}
}

function actionButtonRemoverAnexo() {
	var idArquivo = ""; 
	$(".btn-remover-anexo").click(function(e) {
		idArquivo = $(this).data('id');
		$(this).parents('tr').addClass('opacity');
		
		bootbox.confirm({
			title : 'Anexos',
			message : "Tem certeza que deseja remover esse anexo dessa manifestação ?",
			size : 'medium',
			buttons : {
				confirm : {
					label : 'Confirmar',
					className : 'btn-success outline'
				},

				cancel : {
					label : 'Cancelar',
					className : 'btn-danger outline'
				}
			},

			callback : function(result) {
				if (result) {
					ajaxRemoverAnexo(idArquivo);
				} else {
					$('.opacity').removeClass('opacity');
				}
			}
		});
	});
}

function onChangeTipoAssunto() {
	$("#id_tipo_assunto").change(function() {
		var id_tipo_assunto = $(this).val();
		var idTipoAssuntoHidden = $("#idTipoAssuntoHidden").val();
		
		if(!isNull(id_tipo_assunto) && id_tipo_assunto != idTipoAssuntoHidden) {
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

function ajaxEnviarPedidoComplementacao() {
	$.ajax({
		url : '/painel/manifestacao/enviar_complementacao/',
		type : 'POST',
		data : $("#formComplementacao").serialize(),

		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar enviar o pedido de complementação.", 'Pedido de Complementação');
		},

		success : function(data) {
			toastr.success("Foi enviado o pedido de complementação para o cidadão.", 'Pedido de Complementação');
			window.location.reload();
		},

		complete : function() {
			loadMovimentacoes();
		}
	});
}