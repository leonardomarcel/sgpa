var idSelectEstado = "#id_endereco_estado";
var idSelectMunicipio = "#id_endereco_cidade";
var idSelectBairro = "#id_endereco_bairro";
var idLogradouro = "#id_logradouro";
var idCep = "#id_endereco_cep";

var $selectizeMunicipio;
var $selectizeBairro;
var $selectizeUF;
var idPericiando = "";
	
$(document).ready(function() {
	initializeSelectizeEstado();
	initializeSelectizeMunicipio();
	initializeSelectizeBairro();
	
	onChangeEstado();
	onChangeMunicipio();
	onChangeBairro();
	buscarEnderecoNoViaCep();
	
});

function initializeSelectizeMunicipio() {
	$selectizeMunicipio = $(idSelectMunicipio).selectize({
		maxItems: 1,
		searchField: ['nome'],
		valueField: 'id',
		labelField: 'nome',
		placeholder: 'Pesquise pelo nome',
		options: [],
		preload: true,
	    create: false,
	    selectOnTab: true,
		render: {
		 	item: function(item, escape) {
			       return 	'<div>' +
			                    '<span class="title">' +
			                    '<span class="by">' + escape(item.nome) + '</span>' +
			                    '</span>' +
			              	'</div>';
			   },
			
		   option: function(item, escape) {
		 		 return  '<div>' +
					 		 '<span class="title">' + escape(item.nome) + '</span>' +
	                 	 '</div>';
			   }
		},
	}).data('selectize');
}

function onChangeBairro() {
	$(idSelectBairro).change(function () {
		var id_bairro = $(this).val();
		if(!isNull(id_bairro)) {
			$("#id_0-bairro_id").val(id_bairro);
		}
	});
}

function onChangeMunicipio() {
	$(idSelectMunicipio).change(function () {
		var id_municipio = $(this).val();
		if(!isNull(id_municipio)) {
			$(idSelectMunicipio).val(id_municipio);
			$selectizeBairro.clearOptions();
			$selectizeBairro.enable();
			
			$selectizeBairro.load(function(callback) {
	    		$.getJSON('/basico/bairros_json/'+ id_municipio, function(data) {
					 callback(data);
				}).fail(function() {
					exibirMensagem('Bairros', 'Ocorreu um problema ao tentar carregar os bairros.');
				}).done(function() {
					$selectizeBairro.enable();
				});
	    	});
		}
	});
}

function onChangeEstado() {
	$(idSelectEstado).change(function () {
	    var id_estado = $(this).val();

	    if(!isNull(id_estado)) {
	    	$selectizeMunicipio.clearOptions();
	    	$selectizeMunicipio.enable();
	    	$selectizeMunicipio.load(function(callback) {
	    		
	    		$.getJSON('/basico/cidades_json/'+ id_estado, function(data) {
					 callback(data);
				}).fail(function() {
					exibirMensagem('Cidades', 'Ocorreu um problema ao tentar carregar as cidades.');
				}).done(function() {
					$selectizeMunicipio.enable();
				});
	    	});
	    }
	});
}

function initializeSelectizeEstado() {
	$selectizeUF =  $(idSelectEstado).selectize({
		maxItems: 1,
		valueField: ['id'],
		preload: true,
		searchField: ['nome', 'sigla'],
		labelField: 'nome',
		placeholder: 'Pesquise pelo nome',
	    selectOnTab: true,
	    
	    render: {
		 	item: function(item, escape) {
		       return 	'<div data-sigla='+ item.sigla +'>' +
		                    '<span class="title">' +
		                    	'<span class="by">' + escape(item.nome) + '</span> ' +
		                    '</span>' +
		              	'</div>';
			   },
			
			
		 	option: function(item, escape) {
		 		return 	'<div data-sigla='+ item.sigla +'>' +
		 		 			'<span class="title">' + escape(item.nome) + '</span>' +
	 		 			'</div>';
			   }
		},
	}).data('selectize');
}

function initializeSelectizeBairro() {
	$selectizeBairro = $(idSelectBairro).selectize({
		maxItems: 1,
		searchField: ['nome'],
		valueField: 'id',
		labelField: 'nome',
		placeholder: 'Pesquise pelo nome',
		options: [],
		preload: true,
	    create: false,
	    selectOnTab: true,
		render: {
		 	item: function(item, escape) {
			       return 	'<div>' +
			                    '<span class="title">' +
			                    	'<span class="by">' + escape(item.nome) + '</span> ' +
			                    '</span>' +
			              	'</div>';
			   },
			
		   option: function(item, escape) {
		 		 return  '<div>' +
					 		 '<span class="title">' + escape(item.nome) + '</span>' +
	                 	 '</div>';
			   }
		},
	}).data('selectize');
	
}

function isNull(valor) {
	return valor == undefined || valor == null || $.trim(valor) == '' || valor == 'None';
}

function setCidadeOnSelectizeByCodIbge(cod_ibge) {
	var cidadesOptions = $selectizeMunicipio.options;
	
	$.each(cidadesOptions, function(i, cidade) {
		if(cod_ibge == cidade.cod_ibge) {
			$selectizeMunicipio.setValue(cidade.id);
		}
	});	
}

function buscarEnderecoNoViaCep() {
	$(idCep).focusout(function() {
		var validacep = /^[0-9]{8}$/;
		var cep =$(this).val().replace('-', '');
		
			if(validacep.test(cep)) {
				$.getJSON('https://viacep.com.br/ws/'+ cep +'/json/', function(data) {
					if(data.erro) {
						exibirMensagem('CEP', 'CEP não encontrado');
					} else {
						var cod_ibge = data.ibge;
						$(idLogradouro).val(data.logradouro);
						
						if(!isNull(cod_ibge)) {
							setCidadeOnSelectizeByCodIbge(cod_ibge);
						}
					}
				});
			} else {
				exibirMensagem('CEP', 'CEP inválido');
			}
	});
}

function exibirMensagem(titulo, mensagem) {
	toastr.error(mensagem, titulo);
}