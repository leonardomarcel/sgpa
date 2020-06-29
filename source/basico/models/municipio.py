from django.db import models


import reversion
from util.fields import CharUpperField
from basico.models.pais import Pais

@reversion.register()
class Municipio(models.Model):
    
    nome        = CharUpperField('Nome:', max_length=350)
    pais        = models.ForeignKey(Pais, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s" % (self.nome)
    
    def __unicode__(self):
        return "%s" % self.nome

    class Meta():
        app_label = 'basico'
        ordering  = ['nome',]