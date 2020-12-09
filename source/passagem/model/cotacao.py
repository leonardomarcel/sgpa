# -*- coding: utf-8 -*-
from django.db import models
from passagem.model.passagem import Passagem
from passagem.model.companhia import Companhia


class Cotacao(models.Model):   
    
    passagem             = models.ForeignKey(Passagem, on_delete=models.CASCADE) 
    numero_voo            = models.CharField('Número do Voo', max_length=20)
    valor                 = models.DecimalField('Valor da passagem', max_digits=16, decimal_places=2)
    companhia             = models.ForeignKey(Companhia, related_name="companhia_ida", on_delete=models.CASCADE) 
    data                  = models.DateTimeField("Data da IDA")  