from django.db import models
import reversion


from passagem.model.agencia import Agencia
from passagem.model.rota import Rota
from passagem.model.passageiro_passagem import PassageiroPassagem

@reversion.register()
class RemarcacaoPassagem(models.Model):
    
    data_viagem            = models.DateTimeField()
    data_remarcacao        = models.DateTimeField(null=True,blank=True)
    valor                  = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    multa                  = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    tarifa                 = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    num_bilhete            = models.CharField(max_length=50, null=True,blank=True)
    num_voo                = models.CharField(max_length=50, null=True,blank=True)
    valor_embarque         = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    taxa_servico           = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    passageiro_passagem    = models.ForeignKey(PassageiroPassagem, on_delete=models.CASCADE)
    
    
    class Meta():
        app_label = 'passagem'
        verbose_name = 'Remarcacao'
        verbose_name_plural = 'Remarcacaoß'
        ordering = ('data_viagem',)
        
                                              

    
