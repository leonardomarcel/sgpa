from django.db import models
import reversion


from passagem.model.agencia import Agencia
from passagem.model.rota import Rota
from passagem.model.passageiro import Passageiro
from django.apps import apps


TIPO_CHOICE = (
                 ('I','IDA'),
                 ('V','VOLTA'),
                 )



@reversion.register()
class Passagem(models.Model):
    
    data_viagem            = models.DateTimeField()
    #hora_viagem            = models.TimeField(null=True,blank=True)
    agencia                = models.ForeignKey(Agencia, on_delete=models.CASCADE, null=True,blank=True)
    rota                   = models.ForeignKey(Rota, on_delete=models.CASCADE)
    tipo                   = models.CharField(choices=TIPO_CHOICE, max_length=100)
    urgente                = models.BooleanField(null=True,blank=True, default=False)
    justificativa_urgencia = models.TextField('Justificativa da Urgência',null=True,blank=True)
    
    
    passageiros            = models.ManyToManyField(Passageiro, through="PassageiroPassagem", null=True,blank=True)
    

    def cotacao(self):
        return apps.get_model('passagem.Cotacao').objects.get(passagem=self.pk)

    class Meta():
        app_label = 'passagem'
        verbose_name = 'Passagem'
        verbose_name_plural = 'Passagens'
        ordering = ('data_viagem',)
        
                                              

    