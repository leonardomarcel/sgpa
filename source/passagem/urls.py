#from django.conf.urls import url

from passagem.views.manter_painel import PainelView
from django.urls import path, include

from django.contrib.auth.decorators import login_required
from passagem.views.manter_solicitacao_passagem import SolicitacaoPassagemCreateView,\
    SolicitacaoPassagemRotaCreateView, SolicitacaoPassagemUpdateView,\
    SolicitacaoPassagemPassageiroCreateView, SolicitacaoPassagemListView,\
    AcompanhamentoSolicitacaoPassagemCreateView, SolicitacaoPassagemConclucaoDetailView,\
    SolicitacaoPassagemPassagensDetailView
from passagem.views.manter_passagem import TrechoDeleteView, PassageiroPassagemUpdateView, PassageiroPassagemCreateView, PassageiroPassagemUpdateView,\
    RemarcacaoPassagemCreateView
    
from passagem.views.manter_passageiro import PassageiroCreateView,\
    PassageiroListView, PassageiroUpdateView
from passagem.views.manter_cotacao import CotacaoPassagemCreateView, CotacaoPassagemUpdateView
from passagem.views.manter_cota import CotaCreateView, CotaListView, CotaUpdateView
from passagem.views.manter_aeroporto import AeroportoCreateView, AeroportoListView, AeroportoUpdateView
from passagem.views.manter_rota import RotaCreateView, RotaListView, RotaUpdateView
from passagem.views.manter_agencia_viagem import AgenciaViagemCreateView, AgenciaViagemListView, AgenciaViagemUpdateView
from passagem.views.manter_companhia_aerea import CompanhiaAereaCreateView, CompanhiaAereaListView, CompanhiaAereaUpdateView

app_name = 'passagem'    



urlpatterns = [
    path('index/', PainelView.as_view(), name="passagem"),
    path('solicitacao_passagem/add/', SolicitacaoPassagemCreateView.as_view(), name='solicitacao_passagem_add'),
    path('solicitacao_passagem/update/<int:id_solicitacao_passagem>/', SolicitacaoPassagemUpdateView.as_view(), name="solicitacao_passagem_update"),
    path('solicitacao_passagem_rota/add/<int:id_solicitacao_passagem>/', SolicitacaoPassagemRotaCreateView.as_view(), name="solicitacao_passagem_rota_add"),
    path('solicitacao_passagem_passageiro/add/<int:id_solicitacao_passagem>/', SolicitacaoPassagemPassageiroCreateView.as_view(), name="solicitacao_passagem_passageiro_add"),
    path('solicitacoes_passagem/', SolicitacaoPassagemListView.as_view(), name='solicitacoes_passagem'),
    path('trecho/delete/<int:id_passagem>/<int:id_solicitacao_passagem>/', TrechoDeleteView.as_view(), name="deletar_trecho"),
    path('passageiro/add/', PassageiroCreateView.as_view(), name="passageiro_add"),
    path('passageiro/update/<int:id_passageiro>/', PassageiroUpdateView.as_view(), name="passageiro_update"),
    path('passageiros/', PassageiroListView.as_view(), name='passageiros'),
    path('acompanhamento_solicitacao_passagem/<int:id_solicitacao_passagem>/', AcompanhamentoSolicitacaoPassagemCreateView.as_view(), name="acompanhamento_solicitacao_passagem"),
    path('cotacao/update/<int:id_cotacao>/<int:id_solicitacao_passagem>/', CotacaoPassagemUpdateView.as_view(), name="cotacao_update"),
    path('cotacao/add/<int:id_solicitacao_passagem>/<int:id_passagem>/', CotacaoPassagemCreateView.as_view(), name="cotacao_add"),  
    path('passageiro_passagem/add/<int:id_passageiro>/<int:id_solicitacao_passagem>/<int:id_passagem>/', PassageiroPassagemCreateView.as_view(), name="passageiro_passagem_add"),
    path('passageiro_passagem/update/<int:id_passageiro>/<int:id_passagem>/<int:id_solicitacao_passagem>/', PassageiroPassagemUpdateView.as_view(), name="passageiro_passagem_update"),
    path('cota/add/', CotaCreateView.as_view(), name="cota_add"),
    path('cota/uptade/<int:id_cota>/', CotaUpdateView.as_view(), name="cota_update"),
    path('cotas/', CotaListView.as_view(), name="cotas"),
    path('solicitacao_passagem/datail/<int:pk>', SolicitacaoPassagemConclucaoDetailView.as_view(), name='solicitacao_passagem_conclusao_detail'),
    path('aeroporto/add/', AeroportoCreateView.as_view(), name="aeroporto_add"),
    path('aeroportos/', AeroportoListView.as_view(), name="aeroportos"),
    path('aeroporto/update/<int:id_aeroporto>/', AeroportoUpdateView.as_view(), name="aeroporto_update"),
    path('rota/add/', RotaCreateView.as_view(), name="rota_add"),
    path('rotas/', RotaListView.as_view(), name="rotas"),
    path('rota/uptade/<int:id_rota>/', RotaUpdateView.as_view(), name="rota_update"),
    path('agencia_viagem/add/', AgenciaViagemCreateView.as_view(), name="agencia_viagem_add"),
    path('agencias_viagem/', AgenciaViagemListView.as_view(), name="agencias_viagem"),
    path('agencia_viagem/update/<int:id_agencia_viagem>/', AgenciaViagemUpdateView.as_view(), name="agencia_viagem_update"),
    path('companhia_aerea/add/', CompanhiaAereaCreateView.as_view(), name="companhia_aerea_add"),
    path('companhias_aereas/', CompanhiaAereaListView.as_view(), name="companhias_aereas"),
    path('companhia_aerea/uptade/<int:id_companhia_aerea>/', CompanhiaAereaUpdateView.as_view(), name="companhia_aerea_update"),
    path('solicitacao_passagem_passagens/detail/<int:pk>/', SolicitacaoPassagemPassagensDetailView.as_view(), name='solicitacao_passagem_passagens'),
    path('remarcacao_passagem/add/<int:id_passageiro_passagem>/<int:id_solicitacao_passagem>/', RemarcacaoPassagemCreateView.as_view(), name="remarcacao_passagem_add"),
]