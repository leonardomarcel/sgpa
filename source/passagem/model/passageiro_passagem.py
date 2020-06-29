# -*- coding: utf-8 -*-
from django.db import models
from django.apps import apps
from passagem.model.passagem import Passagem
from passagem.model.passageiro import Passageiro
from passagem.model.companhia import Companhia

STATUS_CHOICE = (
                 ('AG','AGUARDANDO AUTORIZACAO'),
                 ('AUT','AUTORIZADA'),
                 ('C','COMPRADA'),
                 )

        
class PassageiroPassagem(models.Model):
    
    passagem        = models.ForeignKey(Passagem, on_delete=models.CASCADE)
    passageiro      = models.ForeignKey(Passageiro, on_delete=models.CASCADE)
    num_bilhete     = models.CharField(max_length=50, null=True,blank=True)
    num_voo         = models.CharField(max_length=50, null=True,blank=True)
    status          = models.CharField(choices=STATUS_CHOICE, max_length=100)
    companhia       = models.ForeignKey(Companhia, on_delete=models.CASCADE, null=True,blank=True)
    tarifa          = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    valor           = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    valor_embarque  = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    taxa_servico    = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,blank=True)
    data_viagem     = models.DateTimeField(null=True, blank=True)


    def __unicode__(self):
        return u'%s'%self.PassageiroPassagem
    
    
    def remarcacoes(self):
        return apps.get_model('passagem.RemarcacaoPassagem').objects.filter(passageiro_passagem=self.pk)
    
    def orgao(self):
        passagens = []
        passagens.append(self.passagem)
        return apps.get_model('passagem.SolicitacaoPassagem').objects.filter(passagens__in=passagens)[0].orgao
    
    def total(self):
        total = self.valor + self.valor_embarque + self.tarifa + self.taxa_servico 
        return total
    class Meta():
        app_label = 'passagem'
        verbose_name = 'passageiro_passagem'
        verbose_name_plural = 'passageiro_passagem'
