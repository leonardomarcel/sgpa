function confirmExclusao(titulo, url) {
	bootbox.confirm({
	    title: titulo,
	    message: "Esta operação não poderá ser desfeita. Tem certeza que deseja apagar este registro?",
	    size: 'medium',
	    buttons: {
	        confirm: {
	            label: 'Confirmar',
	            className: 'btn-success outline'
	        },
	        
	        cancel: {
	            label: 'Cancelar',
	            className: 'btn-danger outline'
	        }
	    },
	    
	    callback: function (result) {
	    	if(result) {
	    		 window.location = url;
	    	}
	    }
	});
}