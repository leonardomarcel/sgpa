# -*- coding: utf-8 -*-
from django.db import models
from util.fields import CharUpperField
import datetime
from datetime import date


CATEGORIA_CHOICE = (
                 ('is_crianca_1','Criança de 0 a 2 anos'),
                 ('is_crianca_2','Criança de 2 a 12 anos'),
                 ('is_adulto','Pessoa acima de 12 anos'),
                 )
class Passageiro(models.Model):
    
    nome = CharUpperField('Nome', max_length=100)
    cpf  = models.CharField('CPF', max_length=14, unique=True)
    fone = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='Endereço de Email', max_length=255, null=True, blank=True)
    servidor = models.BooleanField(default=True)
    categoria = models.CharField(choices=CATEGORIA_CHOICE, max_length=100)
    data_nascimento = models.DateField()
    
   
    
    def __str__(self):
        
        return '%s, %s' % (self.cpf, self.nome)
    
   
    def idade(self):
        """Retorna a idade em inteiro do passageiro.
    
        """
        anos = []
        ano_nascimento = int(self.data_nascimento.year)
        if date.today().month < self.data_nascimento.month:
            ano_nascimento = ano_nascimento + 1

        for ano in range(ano_nascimento, int(date.today().year)):
            anos.append(ano)
        
        idade = len(anos)
        return idade

    #Crianças de 0 a 2 anos de idade
    def is_crianca_1(self):
        return #retornar resultado do metodo
    
    #Crianças de 2 a 12 anos de idade
    def is_crianca_2(self):
        return #retornar resultado do metodo
    
    #Pessoa acima de 12 anos
    def is_adulto(self):
        return #retornar resultado do metodo
      
    
    def __unicode__(self):
        return self.nome
    
    
#     def num_passagens(self):
#         passagens = get_model('passagem','Passagem_Passageiros').objects.filter(passageiro=self)
#         if passagens:
#             n=passagens.count()
#             if n==1:
#                 return '1 Passagem'
#             else:
#                 return '%s Passagens'%n
#         return ''
         
    class Meta():
        app_label = 'passagem'
        verbose_name = 'Passageiro'
        verbose_name_plural = 'Passageiros'
        ordering = ('nome',)
        
                                                        