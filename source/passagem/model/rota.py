# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from passagem.model.aeroporto import Aeroporto


class Rota(models.Model):
    origem    = models.ForeignKey(Aeroporto,related_name='rota_origem', on_delete=models.CASCADE)
    destino   = models.ForeignKey(Aeroporto,related_name='rota_destino', on_delete=models.CASCADE)

      

     
         
    class Meta():
        app_label = 'passagem'
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'
        