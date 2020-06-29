# -*- coding: utf-8 -*-
from django.db import models
from basico.models.municipio import Municipio


class Aeroporto(models.Model):
    nome      = models.CharField('Nome do Aeroporto', max_length=255)
    cidade    = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    iata      = models.CharField('Código IATA', max_length=5, null=True, blank=True)
    icao      = models.CharField('Código ICAO', max_length=5, null=True, blank=True)
    site      = models.CharField('Página Web', max_length=255, null=True, blank=True)
    latitude  = models.DecimalField('Latitude', max_digits=16, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Latitude', max_digits=16, decimal_places=6, null=True, blank=True)
    
    
    def __str__(self):
        
        return '%s - %s' % (self.iata, self.nome)
    
    def __unicode__(self):
        return self.nome
    
    
    def ver_site(self):
        return 'http://www.flightstats.com%s'%self.site

    
    def ver_mapa(self):
        return 'http://maps.google.com.br/maps?ll=%s,%s'%(self.latitude,self.longitude)
         
    class Meta():
        app_label = 'passagem'
        verbose_name = 'Aeroporto'
        verbose_name_plural = 'Aeroportos'
        ordering = ('nome',)
        
                                            