/**
 *  Personalizando as propriedades do toast
 */
$(document).ready(function() {
	configureToastr();
});

function configureToastr() {
	toastr.options = {
			'closeButton': true,
			'debug': false,
			'newestOnTop': false,
			'progressBar': false,
			"positionClass": "toast-top-right",
			'preventDuplicates': true,
			'onclick': null,
			'showEasing': 'swing',
			'hideEasing': 'linear',
			'showMethod': 'fadeIn',
			'hideMethod': 'fadeOut'
	}
}

