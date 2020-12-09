$(document).ready(function() {
	ajaxFormLogin();
});

function ajaxFormLogin() {
	$("#formLoginCidadao").submit(function(event) {
		 var loading = $("#loading").clone();
		 loading.removeAttr("id");
		 loading.removeClass('d-none');
		 loading.find('#textoLoading').text('Autenticando cidadão');
		 loading.find('i').addClass('fa-5x').removeClass('fa-10x');
		
		$('.is-invalid').removeClass('is-invalid');
		$(".invalid-feedback").remove();
		
	    event.preventDefault(); //prevent default action 
	    var post_url = $(this).attr("action"); //get form action url
	    var request_method = $(this).attr("method"); //get form GET/POST method
	    var form_data = $(this).serialize(); //Encode form elements for submission
	    var email = $("#login_email").val();
	    var senha = $("#login_senha").val();
	    var is_ok = new Boolean('true');
	    var div_invalid = $("<div class='invalid-feedback'>* Este campo é obrigatório.</div>");

	    if(isNull(email)) {
	    	$("input[name='email']").addClass('is-invalid');
	    	$(".input-group-email").after($(div_invalid).clone(true));
	    	is_ok = false;
	    	$("input[name='email']").focus();
	    }
	    
	    if(isNull(senha)) {
	    	$("input[name='senha']").addClass('is-invalid');
	    	$(".input-group-senha").after($(div_invalid).clone(true));
	    	is_ok = false;
	    }
	    
	    if(is_ok) {
	    	$("#formLoginCidadao").find(".icon-ajax").remove();
		    $.ajax({
		        url : post_url,
		        type: request_method,
		        data : decodeURI(form_data),
		       
		        beforeSend: function() {
		        	$("#formLoginCidadao").append($(loading).clone(true));	
		        },
		        
		        success: function(data) {
		        	toastr.success('Autenticação efetuada com sucesso.', 'Autenticação');
		        	location.reload();
				},
				
				error: function(error) {
					$("#formLoginCidadao").find(".icon-ajax").remove();
					  if (error.status == 406) {
						toastr.error('Usuário e/ou senha inválido(s).', 'Autenticação');
					  } else if (error.status == 402) {
						  toastr.error('Usuário desativado.', 'Autenticação');
					  } else {
						  toastr.error('Ocorreu um problema ao tentar autenticar.', 'Autenticação');
					  }
				}   
		    });
	    }
	});
}
