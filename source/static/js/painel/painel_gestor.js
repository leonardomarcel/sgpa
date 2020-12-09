$(document).ready(function() {
	$('#sparkbar').sparkline([ [6], [5], [7], [8] ], {type: 'bar'});
    $('#sparkline').sparkline([10,8,5,7,4,4,1], {type: 'line', lineColor: 'red'});
    $('#sparkpie').sparkline([10,8,5,7,4,4,1], {type: 'pie'});
    highChartsManifestacao();
});

function highChartsManifestacao() {
	  var ctx = document.getElementById("myChart").getContext('2d');
	  var myChart = new Chart(ctx, {
	      type: 'bar',
	      data: {
	          labels: ["Denúncias", "Reclamações", "Solicitações", "Sugestões", "Elogios", "Fora do Escopo"],
	          datasets: [{
	              label: 'Total',
	              data: [total_denuncia, total_reclamacao, total_solicitacao, total_sugestao, total_elogio, total_fora_escopo],
	              borderWidth: 0,
	              backgroundColor: '#4DD0E1'
	          }]
	      },
	      options: {
	          scales: {
	              xAxes: [{
	                ticks: {
	                  display: true,
	                  fontColor: '#fff'
	                },
	                gridLines: {
	                  display: false,
	                  drawBorder: false
	                }
	              }],
	              yAxes: [{
	                  ticks: {
	                      beginAtZero:true,
	                      display: false
	                  },
	                  gridLines: {
	                    display: false,
	                    drawBorder: false
	                  }
	              }]
	          },
	          legend: {
	            display: false
	          }
	      }
	      
	  });

	      var MONTHS = months_name;
	      var COUNTS = months_count;
	      
	      var config = {
	          type: 'line',
	          data: {
	              labels: MONTHS,
	              datasets: [{
	                  label: "Manifestações",
	                  backgroundColor: '#C62828',
	                  borderColor: '#D32F2F',
	                  data: COUNTS,
	                  fill: false,
	              }]
	          },
	          options: {
	              responsive: true,
	              tooltips: {
	                  mode: 'index',
	                  intersect: false,
	              },
	              hover: {
	                  mode: 'nearest',
	                  intersect: true
	              },
	              scales: {
	                  xAxes: [{
	                      display: true,
	                      gridLines: {
	                        display: false,
	                        drawBorder: false
	                      }
	                  }],
	                  yAxes: [{
	                      display: false,
	                      gridLines: {
	                        drawBorder: false
	                      }
	                  }]
	              },
	              legend: {
	                display: false
	              }
	          }
	      };

		ctx = document.getElementById("chartAtendimentos").getContext("2d");
		var chartAtendimentos = new Chart(ctx, config);
}