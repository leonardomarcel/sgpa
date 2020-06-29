# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from passagem.model.aeroporto import Aeroporto
from passagem.model.solicitacao_passagem import SolicitacaoPassagem
from passagem.model.passagem import Passagem


class Trecho(models.Model):
    solicitacao_passagem    = models.ForeignKey(SolicitacaoPassagem, on_delete=models.CASCADE)
    passagens               = models.ManyToManyField(Passagem)
    tipo                    = models.CharField( max_length=100)
      

     
         
    class Meta():
        app_label = 'passagem'
        verbose_name = 'Trecho'
        verbose_name_plural = 'Techos'