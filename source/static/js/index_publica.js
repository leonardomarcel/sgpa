var is_manifestacao_anonima;
$(document).ready(function() {
	copyToClipboard();
	is_manifestacao_anonima = !isNull($("#tokenText").text());
	
	if(is_manifestacao_anonima) {
		showMessageToken();
	}
});

function showMessageToken() {
	var token = $("#tokenText").text();
	var div_token = $("#divMensagemToken").clone().removeAttr('id');
		div_token.removeClass('hide');
		div_token.find("#spanTokenModal").text(token);
		bootbox.dialog({
	    title: "Manifestação Enviada",
	    message: div_token,
	    closeButton: false,
	    
	    	buttons: {
		    	ok: {
		            label: "Entendi",
		            className: 'btn-success',
		            callback: function(){
		                toastr.info('Não esqueça de copiar o <strong>token</strong> ');
		            },
	    	},
	    }
	});
}

function scrollToInputToken() {
	$('html, body').animate({
		scrollTop: $("#formTokenManifestacao").height()
		
	}, 1000);
}

function copyToClipboard() {
	 $("#buttonCopyToken").click(function(){
		 var input = document.createElement('input');
		 var token = $("#tokenText").text();
		 input.setAttribute('value', token);
		 document.body.appendChild(input);
		 input.select();
		 
		 var result = document.execCommand('copy');
		 document.body.removeChild(input);
		 toastr.success('Token <strong>' + token + '</strong> copiado.', 'Token');
		 scrollToInputToken();
		 $("#token_manifestacao").val(token);
		 $("#token_manifestacao").focus();
		 
		 return result;
	 });
}