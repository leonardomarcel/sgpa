$(document).ready(function(){
	modalWindow();
});

function modalWindow() {
  	$('#modalWindow').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget);
		var tituloModal = isNull(button.data('title')) ? 'Detalhes' : button.data('title');
		var modal = $(this);
		
		 var loading = $("#loading").clone();
			loading.removeAttr("id");
			loading.removeClass('hide');
			loading.find('#textoLoading').text('Carregando...');
			loading.find('i').addClass('fa-10x').removeClass('fa-5x');
		
			modal.find('.modal-title').text(tituloModal);
			modal.find('.modal-body').html($('<div class="text-center div-loading"/>').append(loading));
			
			$("<div class=''/>").load(button.data('href'), function() {
				modal.find('.modal-body').html($(this));
			});
	
	}).on('hide.bs.modal', function (e) {
		$(this).find('.modal-title').text('');
		
	});
}