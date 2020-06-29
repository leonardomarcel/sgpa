# -*- coding: utf-8 -*-
from django.db import models
from basico.models.orgao import Orgao
from auth_local.models.usuario_orgao import UsuarioOrgao


EXECICIO_CHOICE = (
    ('2017', '2017'),
    ('2018', '2018'),
    ('2019', '2019'),
    ('2020', '2020'),
    ('2021', '2021'),
    ('2022', '2022'),
    ('2023', '2023'),
  )                    

class Cota(models.Model):
    
    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    exercicio = models.CharField(choices = EXECICIO_CHOICE, max_length=4)
    inicio = models.DateField("Inicio")
    termino = models.DateField("Termino")
    usuario_criacao = models.ForeignKey(UsuarioOrgao, on_delete=models.CASCADE)
    
    
    class Meta():
        app_label = 'passagem'
        verbose_name = 'Cota'
        verbose_name_plural = 'Cotas'
        unique_together = ('orgao', 'exercicio')