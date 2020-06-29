from django.db import models
import reversion

@reversion.register()
class Agencia(models.Model):
    nome                   = models.CharField(max_length=100)
    cnpj                   = models.CharField(max_length=18)
    inscricao_estadual     = models.CharField(max_length=100)
    nome_fantasia          = models.CharField(max_length=100)
    contrato               = models.CharField(max_length=100)
    fone                   = models.CharField(max_length=15)
    fax                    = models.CharField(max_length=13)
    email                  = models.EmailField()
    homepage               = models.CharField(max_length=13)     
    
    def __str__(self):
        return "%s" % (self.nome)

    