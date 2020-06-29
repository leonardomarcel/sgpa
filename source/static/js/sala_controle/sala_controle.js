var is_ouvidoria_selected;
$(document).ready(function() {
	actionButtonLimparFiltro();
	is_ouvidoria_selected = false;
	highChartsTipoManifestacao();
    highChartsOuvidorias();
    highChartsStatus();
    highChartsIdentificacao();
    highChartsPrazoManifestacao();
    initializeSelectize();
    $('[data-toggle=popover]').popover({
		trigger: 'hover',
		placement: 'top',
		html: true
	});
    datePicker();
    $('.date-picker').mask('99/99/9999');
    actionButtonExportTipoIdentificacao();
    actionButtonFiltroSalaControle();
});

function initializeSelectize() {
	$('#id_ouvidoria').selectize({
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		multiple: true,
		maxItems: null,
		placeholder: 'Selecione...',
		selectOnTab: true,
	});	
	
	$('#id_tipo_manifestacao').selectize({
		searchField: 'nome',
		valueField: 'id',
		labelField: 'nome',
		maxItems: null,
		placeholder: 'Selecione...',
		selectOnTab: true,
	});	
}

function highChartsTipoManifestacao() {
	   gradientBarChartConfiguration =  {
		        maintainAspectRatio: false,
		        legend: {
		              display: false
		         },

		         tooltips: {
		           backgroundColor: '#1f8ef1',
		           titleFontColor: '#fff',
		           bodyFontColor: '#fff',
		           bodySpacing: 4,
		           xPadding: 4,
		           mode: "nearest",
		           intersect: 0,
		           position: "nearest"
		         },
		         responsive: true,
		         
		         
		         
		         scales:{
		           yAxes: [{

		                 gridLines: {
		                   drawBorder: false,
		                     color: 'rgba(29,140,248,0.1)',
		                     zeroLineColor: "transparent",
		                 },
		                 ticks: {
		                     suggestedMin: 60,
		                     suggestedMax: total_manifestacoes,
		                     padding: 5,
		                     fontColor: "#9e9e9e"
		                 }
		               }],

		           xAxes: [{

		                 gridLines: {
		                   drawBorder: false,
		                     color: 'rgba(29,140,248,0.1)',
		                     zeroLineColor: "transparent",
		                 },
		                 ticks: {
		                     padding: 20,
		                     fontColor: "#9e9e9e"
		                 }
		               }]
		           }
		      };
	 var ctx = document.getElementById("myChartManifestacoes").getContext("2d");

  var gradientStroke = ctx.createLinearGradient(0,230,0,50);

  gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
  gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.5)');
  gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


  var myChart = new Chart(ctx, {
    type: 'line',
    responsive: true,
    legend: {
          display: false
    },
    data: {
      labels: ["Denúncias", "Reclamações", "Solicitações", "Sugestões", "Elogios"],
      datasets: [{
        label: "Total",
        fill: true,
        backgroundColor: gradientStroke,
        hoverBackgroundColor: gradientStroke,
        borderColor: '#1f8ef1',
        borderWidth: 2,
        borderDash: [],
        borderDashOffset: 0.0,
        data: [total_denuncia, total_reclamacao, total_solicitacao, total_sugestao, total_elogio],
      }]
    },
      options: gradientBarChartConfiguration
  });
}


function highChartsOuvidorias() {
	
	   gradientBarChartConfiguration =  {
		        maintainAspectRatio: false,
		        legend: {
		              display: false
		         },

		         tooltips: {
	        	   backgroundColor: '#1f8ef1',
			       titleFontColor: '#fff',
			       bodyFontColor: '#fff',
		           bodySpacing: 4,
		           xPadding: 12,
		           mode: "nearest",
		           intersect: 0,
		           position: "nearest"
		         },
		         responsive: true,
		         scales:{
		           yAxes: [{

		                 gridLines: {
		                   drawBorder: false,
		                     color: 'rgba(29,140,248,0.1)',
		                     zeroLineColor: "transparent",
		                 },
		                 ticks: {
		                     suggestedMin: 60,
		                     suggestedMax: total_manifestacoes,
		                     padding: 5,
		                     fontColor: "#9e9e9e"
		                 }
		               }],

		           xAxes: [{

		                 gridLines: {
		                   drawBorder: false,
		                     color: 'rgba(29,140,248,0.1)',
		                     zeroLineColor: "transparent",
		                 },
		                 ticks: {
		                     padding: 20,
		                     fontColor: "#9e9e9e"
		                 }
		               }]
		           }
		      };
	 var ctx = document.getElementById("myChartOuvidorias").getContext("2d");

     var gradientStroke = ctx.createLinearGradient(0,230,0,50);

     gradientStroke.addColorStop(1, 'rgba(29,140,248,0.5)');
     gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.1)');
     gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

     var myChart = new Chart(ctx, {
       type: 'line',
       responsive: true,
       legend: {
             display: false
       },
       data: {
         labels: orgaos_names,
         datasets: [{
           label: "Total",
           fill: true,
           backgroundColor: gradientStroke,
           hoverBackgroundColor: gradientStroke,
           borderColor: '#1f8ef1',
           borderWidth: 2,
           borderDash: [],
           borderDashOffset: 0.0,
           data: orgaos_count,
         }]
       },
         options: gradientBarChartConfiguration
     });
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

function highChartsStatus() {
	
	var ctx = document.getElementById("myChartStatus").getContext("2d");

    var gradientStroke = ctx.createLinearGradient(0,230,0,50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.7)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

    var myChart = new Chart(ctx, {
      type: 'bar',
      responsive: true,
      legend: {
            display: false
      },
      data: {
    	  labels: ["Cadastradas", 
			 	 "Em análise", 
			 	 "Complementadas", 
			 	 "Prorrogada", 
			 	 "Prazo Vencido",
			 	 "Arquivada",
			 	 "Encerrada"],
        datasets: [{
          label: "Total",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 1.0,
          data: [total_status_cadastradas, 
			   	 total_status_andamento, 
			   	 total_status_complementadas, 
			   	 total_status_prorrogada, 
			   	 total_status_prazo_vencido, 
			   	 total_status_arquivada,
			   	 total_status_encerrada],
        }]
      },
        options: gradientBarChartConfiguration
    });
}

function highChartsIdentificacao() {
	var ctx = document.getElementById("myChartIdentificacao").getContext("2d");
    var gradientStroke = ctx.createLinearGradient(0,230,0,50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.5)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors

    var myChart = new Chart(ctx, {
      type: 'line',
      responsive: true,
      legend: {
            display: false
      },
      data: {
    	labels: ["Identificadas", "Não Identificadas"],
        datasets: [{
          label: "Total",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 1.0,
          data: [total_identificadas, 
        	  	 total_nao_identificadas
        	  	]
        }]
      },
        options: gradientBarChartConfiguration
    });
}


function highChartsPrazoManifestacao() {
	
	var ctx = document.getElementById("myChartPrazoManifestacao").getContext("2d");

    var gradientStroke = ctx.createLinearGradient(0,230,0,50);

    gradientStroke.addColorStop(1, 'rgba(29,140,248,0.5)');
    gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.1)');
    gradientStroke.addColorStop(0, 'rgba(29,140,248,0.1)'); //blue colors

    var myChart = new Chart(ctx, {
      type: 'bar',
      responsive: true,
      
      legend: {
            display: false
      },
      
      data: {
    	  labels: ["Até 01 dia", 
			 	 "02 a 10 dias", 
			 	 "11 a 20 dias", 
			 	 "21 a 30 dias", 
			 	 "Acima de 30 dias",
			 	 "Em Tramitação"],
        datasets: [{
          label: "Total",
          fill: true,
          backgroundColor: gradientStroke,
          hoverBackgroundColor: gradientStroke,
          borderColor: '#1f8ef1',
          borderWidth: 2,
          borderDash: [],
          borderDashOffset: 1.0,
          data: [total_01_day, 
        	  	 total_10_days, 
        	  	 total_20_days, 
        	  	 total_30_days, 
        	  	 total_acima_30_days, 
        	  	 total_andamento
			   	],
        }]
      },
        options: gradientBarChartConfiguration
    });
}

function beforePrintHandler () {
  for (var id in Chart.instances) {
    Chart.instances[id].resize()
  }
}

function actionButtonLimparFiltro() {
	$("#btnLimparFiltro").click(function () {
		window.location.reload()
	});
}

function actionButtonExportTipoIdentificacao() {
	$(".btn-export-image").click(function () {
		beforePrintHandler();
		var id_canvas = $(this).data('id');
		var url_base64jp = document.getElementById(id_canvas).toDataURL("image/jpg");
		var w = window.open('about:blank', 'image from canvas');
		w.document.write("<img src='" + url_base64jp + "' alt='export gráfico por identificação'/>");
	});
}


function actionButtonFiltroSalaControle() {
	$("#btnFiltroGrafico").click(function () {
		var id_grafico = $("#id_tipo_grafico").val();
		var id_ouvidoria = $("#id_ouvidoria").val();
		
		if(id_ouvidoria) {
			is_ouvidoria_selected = true;
		}
		
		$(".card.card-grapich").addClass('activated');
		if(id_grafico==0) {
			$("#formFiltroGrafico").submit();
		} else {
			if(id_grafico==1) {
				$(".card.card-grapich.tipo-manifestacao").removeClass('activated');
				$(".card.card-grapich.prazo").removeClass('activated');
				$(".card.card-grapich.identificacao").removeClass('activated');
				$(".card.card-grapich.ouvidorias").removeClass('activated');
				ajaxFiltroStatus();
			} else if(id_grafico==2) {
				$(".card.card-grapich.status").removeClass('activated');
				$(".card.card-grapich.prazo").removeClass('activated');
				$(".card.card-grapich.identificacao").removeClass('activated');
				$(".card.card-grapich.ouvidorias").removeClass('activated');
				ajaxFiltroTipoManifestacao();
			} else if(id_grafico==3) {
				$(".card.card-grapich.status").removeClass('activated');
				$(".card.card-grapich.tipo-manifestacao").removeClass('activated');
				$(".card.card-grapich.identificacao").removeClass('activated');
				$(".card.card-grapich.ouvidorias").removeClass('activated');
				ajaxFiltroPrazoManifestacao();
			} else if(id_grafico==4) {
				$(".card.card-grapich.ouvidorias").removeClass('activated');
				$(".card.card-grapich.status").removeClass('activated');
				$(".card.card-grapich.prazo").removeClass('activated');
				$(".card.card-grapich.tipo-manifestacao").removeClass('activated');
				ajaxFiltroIdentificacaoManifestacao();
			} else if(id_grafico==5) {
				ajaxFiltroOuvidorias();
				$(".card.card-grapich.prazo").removeClass('activated');
				$(".card.card-grapich.status").removeClass('activated');
				$(".card.card-grapich.identificacao").removeClass('activated');
				$(".card.card-grapich.tipo-manifestacao").removeClass('activated');
			}
		}
	});
}

function showLoading(idCardBody) {
	
	 var loading = $("#loading").clone();
	 loading.removeAttr("id");
	 loading.removeClass('d-none');
	 loading.find('#textoLoading').text('Carregando...');
	 loading.find('i').addClass('fa-10x').removeClass('fa-5x');
	 
	 $("#" + idCardBody).html($('<div class="text-center div-loading"/>').append(loading));
}

function ajaxFiltroStatus() {
	$.ajax({
		type: 'POST',
		url: '/sala-controle/grafico-status/',
		data: $("#formFiltroGrafico").serialize(),
			 
		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar buscar o filtro de status.", 'Filtro');
		},

		beforeSend : function() {
			showLoading('cardBodyGrapichStatus');
		},

		success : function(data) {
			$("#cardBodyGrapichStatus").html(data);
			highChartsStatus();
			$('html, body').animate({
				scrollBottom : $("#cardBodyGrapichStatus").offset().top
			}, 1000);
		},
		complete: function() {
			if(is_ouvidoria_selected) {
				$(".card-header.status").append('Filtro aplicado para: <strong><span class="text-white"> '+ $("#id_ouvidoria option:selected").text() + "</span></strong>");
			}
			is_ouvidoria_selected = false;
		}
	});
}


function ajaxFiltroTipoManifestacao() {
	$.ajax({
		type: 'POST',
		url: '/sala-controle/grafico-tipo-manifestacao/',
		data: $("#formFiltroGrafico").serialize(),
			 
		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar buscar o filtro de status.", 'Filtro');
		},

		beforeSend : function() {
			showLoading('cardBodyGrapichTipoManifestacao');
		},

		success : function(data) {
			$("#cardBodyGrapichTipoManifestacao").html(data);
			highChartsTipoManifestacao();
			$('html, body').animate({
				scrollTop : $("#cardBodyGrapichTipoManifestacao").offset().top
			}, 1000);
		},
		
		complete: function() {
			if(is_ouvidoria_selected) {
				$(".card-header.tipo-manifestacao").append('Filtro aplicado para: <strong><span class="text-white"> '+ $("#id_ouvidoria option:selected").text() + "</span></strong>");
			}
			is_ouvidoria_selected = false;
		}
	});
}

function ajaxFiltroPrazoManifestacao() {
	$.ajax({
		type: 'POST',
		url: '/sala-controle/grafico-prazo-manifestacao/',
		data: $("#formFiltroGrafico").serialize(),
			 
		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar buscar o filtro de status.", 'Filtro');
		},

		beforeSend : function() {
			showLoading('cardBodyGrapichPrazoManifestacao');
		},

		success : function(data) {
			$("#cardBodyGrapichPrazoManifestacao").html(data);
			highChartsPrazoManifestacao();
			$('html, body').animate({
				scrollTop : $("#cardBodyGrapichPrazoManifestacao").offset().top
			}, 1000);
		},
		
		complete: function() {
			if(is_ouvidoria_selected) {
				$(".card-header.prazo").append('Filtro aplicado para: <strong><span class="text-white"> '+ $("#id_ouvidoria option:selected").text() + "</span></strong>");
			}
			is_ouvidoria_selected = false;
		}
	});
}

function ajaxFiltroIdentificacaoManifestacao() {
	$.ajax({
		type: 'POST',
		url: '/sala-controle/grafico-identificacao-manifestacao/',
		data: $("#formFiltroGrafico").serialize(),
			 
		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar buscar o filtro de status.", 'Filtro');
		},

		beforeSend : function() {
			showLoading('cardBodyGrapichIdentificacao');
		},

		success : function(data) {
			$("#cardBodyGrapichIdentificacao").html(data);
			highChartsIdentificacao();
			$('html, body').animate({
				scrollTop : $("#cardBodyGrapichIdentificacao").offset().top
			}, 1000);
		},
		
		complete: function() {
			if(is_ouvidoria_selected) {
				$(".card-header.identificacao").append('Filtro aplicado para: <strong><span class="text-white"> '+ $("#id_ouvidoria option:selected").text() + "</span></strong>");
			}
			is_ouvidoria_selected = false;
		}
	});
}

function ajaxFiltroOuvidorias() {
	$.ajax({
		type: 'POST',
		url: '/sala-controle/grafico-ouvidorias/',
		data: $("#formFiltroGrafico").serialize(),
			 
		error : function(a, b, c) {
			toastr.error("Ocorreu um problema ao tentar buscar o filtro de status.", 'Filtro');
		},

		beforeSend : function() {
			showLoading('cardBodyGrapichOuvidorias');
		},

		success : function(data) {
			$("#cardBodyGrapichOuvidorias").html(data);
			highChartsOuvidorias();
			$('html, body').animate({
				scrollTop : $("#cardBodyGrapichOuvidorias").offset().top
			}, 1000);
		},
		
		complete: function() {
			if(is_ouvidoria_selected) {
				$(".card-header.ouvidorias").append('Filtro aplicado para: <strong><span class="text-white"> '+ $("#id_ouvidoria option:selected").text() + "</span></strong>");
			}
			
			is_ouvidoria_selected = false;
		}
	});
}

function isNull(valor) {
	return valor == undefined || valor == null || $.trim(valor) == '' || valor == 'None';
}

