from django.contrib import admin
from passagem.model.aeroporto import Aeroporto
from passagem.model.agencia import Agencia
from passagem.model.autorizacao import Autorizacao
from passagem.model.companhia import Companhia
from passagem.model.cota import Cota
from passagem.model.historico import Historico
from passagem.model.motivo import Motivo
from passagem.model.passageiro import Passageiro
from passagem.model.passagem import Passagem
from passagem.model.rota import Rota
from passagem.model.solicitacao_passagem import SolicitacaoPassagem



admin.site.register(Aeroporto)
admin.site.register(Agencia)
admin.site.register(Autorizacao)
admin.site.register(Companhia)
admin.site.register(Cota)
admin.site.register(Historico)
admin.site.register(Motivo)
admin.site.register(Passageiro)
admin.site.register(Passagem)
admin.site.register(Rota)
admin.site.register(SolicitacaoPassagem)
