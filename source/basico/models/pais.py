from django.db import models

import reversion
from util.fields import CharUpperField

@reversion.register()
class Pais(models.Model):
    
    nome        = CharUpperField('Nome:', max_length=350)
    sigla        = CharUpperField('Sígla', max_length=2)
    
    def __str__(self):
        return "%s" % (self.nome)
    
    def __unicode__(self):
        return "%s" % self.nome

    class Meta():
        app_label = 'basico'
        