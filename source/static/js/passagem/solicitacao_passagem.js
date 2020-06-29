function change(tipoPassagem){
	var $tipoPassage = $(tipoPassagem).find('select');
	var this_data_volta = $tipoPassage.closest('.form-row').find('#div_volta')
	var this_input_data_volta = $tipoPassage.closest('.form-row').find('.data_volta')
	var val = $tipoPassage.val();
	if (val == 'IV'){
		this_data_volta.show();
	}
	else {
		this_data_volta.hide();
		this_input_data_volta.val('');
		
	};
	
};

$(document).ready(function() {
	var e = document.getElementById("id_tipo");
	var x = document.getElementById("div_volta");
	if (e.value == 'IV'){
		x.style.display = "block";
	}

});

function upperCaseF(a){
    setTimeout(function(){
        a.value = a.value.toUpperCase();
    }, 1);
}

$('#div_volta').hide();







