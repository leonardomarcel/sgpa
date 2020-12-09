#from django.conf.urls import url


from django.urls import path, include

from django.contrib.auth.decorators import login_required
from relatorio.views import MyModelPrintView, generate_pdf
from relatorio.views import RelatorioPassagemPeriodo, RelatorioContabilPassagemPeriodo

app_name = 'relatorio'    



urlpatterns = [
    path('passagem_emitida/detail/<pk>/', MyModelPrintView.as_view(), name='passagem_emitida_detail'),
    path('passagem_emitida_teste/detail/<int:id_passageiro_passagem>/', generate_pdf, name='passagem_emitida_detail_teste'),
    path('form_passagem_periodo/', RelatorioPassagemPeriodo.as_view(), name='form_passagem_periodo'),
    path('form_passagem_periodo_contabil/', RelatorioContabilPassagemPeriodo.as_view(), name='form_passagem_periodo_contabil'),
    
]