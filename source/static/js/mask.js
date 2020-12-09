var tipoError = 'error'
var tipoSuccess = 'success';
var tipoAlert = 'alert';
var tipoInfo =  'info';

$(document).ready(function(){
	maskPhone();
	focusOutCPF();
	datePicker();
	initializeSelectize();
	$('.cep').mask('99999-999');
	$('.cpf').mask('999.999.999-99');
	$('.rg').mask('999999999999999');
	$('.date-picker').mask('99/99/9999');
	$('.cep').attr('placeholder', '99999-999');
	$('.cpf').attr('placeholder', '999.999.999-99');
	$('.date-picker').attr('placeholder', 'dd/mm/yyyy');
	$('[data-toggle="tooltip"]').tooltip();
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

function maskPhone() {
	var masks = ['(00) 00000-0000', '(00) 00000-0009']
	var maskPhoneBehavior = function (val) {
		  return val.replace(/\D/g, '').length === 9 ? masks[0] : masks[1];
		},
		options = {
		  onKeyPress: function(val, e, field, options) {
		      field.mask(maskPhoneBehavior.apply({}, arguments), options);
		    }
		};

		$('.telefone').mask(maskPhoneBehavior, options);
}

function focusOutCPF() {
	$('.cpf').focusout(function() {
		$(this).removeClass('required-color');
		
		if(!isNull($(this).val())) {
			var cpf = get_numbers_cpf_or_pis($(this).val());
			if(!isCPFValid(cpf)) {
				exibirMensagem('CPF', 'O CPF informado é inválido', tipoError);
				$(this).addClass('required-color');
			}  
		}
	});
}

function get_numbers_cpf_or_pis(string) {
	var novoCPF = string.replace(/[\.-]/g, "");
	return novoCPF;
}

function isCPFValid(cpf) {  
    if(isNull(cpf)) return false; 
    // Elimina CPFs invalidos conhecidos    
    if (cpf.length != 11 || 
        cpf == "00000000000" || 
        cpf == "11111111111" || 
        cpf == "22222222222" || 
        cpf == "33333333333" || 
        cpf == "44444444444" || 
        cpf == "55555555555" || 
        cpf == "66666666666" || 
        cpf == "77777777777" || 
        cpf == "88888888888" || 
        cpf == "99999999999")
            return false;       
    // Valida 1o digito 
    add = 0;    
    for (i=0; i < 9; i ++)       
        add += parseInt(cpf.charAt(i)) * (10 - i);  
        rev = 11 - (add % 11);  
        if (rev == 10 || rev == 11)     
            rev = 0;    
        if (rev != parseInt(cpf.charAt(9)))     
            return false;       
    // Valida 2o digito 
    add = 0;    
    for (i = 0; i < 10; i ++)        
        add += parseInt(cpf.charAt(i)) * (11 - i);  
    rev = 11 - (add % 11);  
    if (rev == 10 || rev == 11) 
        rev = 0;    
    if (rev != parseInt(cpf.charAt(10)))
        return false;       
    return true;   
}

function exibirMensagem(titulo, mensagem, tipo) {
	if(tipo == tipoSuccess) {
		toastr.success(mensagem, titulo);
	} 
	
	if(tipo == tipoAlert) {
		toastr.warning(mensagem, titulo);
	} 
	
	if(tipo == tipoError) {
		toastr.error(mensagem, titulo);
	}

	if(tipo == tipoInfo) {
		toastr.info(mensagem, titulo);
	}
}

function datePicker() {
	habilitarDatePicker();
	focarDatePicker();
}

function habilitarDatePicker() {
	$('[class*=date-picker]').datepicker({
		autoclose: true,
		language: 'pt-BR',
		maxDate: new Date(),
   	   	format: 'dd/mm/yyyy'
	});
}

function focarDatePicker() {
	$('span[id*=datepicker]').on('click', function() {
		$(this).parent('div').find('input').focus();
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