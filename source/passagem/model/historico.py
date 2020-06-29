from django.db import models
import reversion

from passagem.model.solicitacao_passagem import SolicitacaoPassagem
from auth_local.models.usuario_orgao import UsuarioOrgao




@reversion.register()
class Historico(models.Model):
    
    data                   = models.DateTimeField()
    solicitacao_passagem   = models.ForeignKey(SolicitacaoPassagem, on_delete=models.CASCADE)
    usuario                = models.ForeignKey(UsuarioOrgao, on_delete=models.CASCADE)
    descricao = models.TextField('Descrição',null=True,blank=True)
    
    
    def __str__(self):
        return "%s" % (self.usuario)

    