from django.db import models
import reversion
from auth_local.models.usuario_orgao import UsuarioOrgao





@reversion.register()
class Autorizacao(models.Model):
    
    data                   = models.DateTimeField()
    usuario                = models.ForeignKey(UsuarioOrgao, on_delete=models.CASCADE)
    observacao = models.TextField('Observação',null=True,blank=True)
    
    
    def __str__(self):
        return "%s" % (self.usuario)

    