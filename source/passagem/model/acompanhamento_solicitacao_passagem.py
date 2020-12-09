import os
from django.conf import settings
from django.db import models
import reversion

from basico.models.orgao import Orgao
from passagem.model.motivo import Motivo
from auth_local.models.usuario_orgao import UsuarioOrgao
from datetime import datetime
from passagem.model.passagem import Passagem
from passagem.model.solicitacao_passagem import SolicitacaoPassagem

STATUS_CHOICE = (
                 ('COM PENDENCIA','COM PENDENCIA'),
                 ('AUTORIZADA','AUTORIZADA'),
                 )


@reversion.register()
class AcompanhamentoSolicitacaoPassagem(models.Model):
    
    data                   = models.DateTimeField(null=True,blank=True)
    usuario                = models.ForeignKey(UsuarioOrgao, on_delete=models.CASCADE, null=True,blank=True)
    descricao              = models.TextField('Descrição do Evento')
    solicitacao_passagem   = models.ForeignKey(SolicitacaoPassagem, on_delete=models.CASCADE)
    status                 = models.CharField(choices=STATUS_CHOICE, max_length=40)