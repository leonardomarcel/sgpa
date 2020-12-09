from django.db import models
import reversion

'''
IATA - International Air Transport Association
ICAO - International Civil Aviation Organization  
'''

@reversion.register()
class Companhia(models.Model):
    
    nome                   = models.CharField(max_length=100)
    iata                   = models.CharField(max_length=5)
    icao                   = models.CharField(max_length=5, null=True, blank=True)
    fone1                  = models.CharField('Telefone', max_length=15, null=True, blank=True)
    fone                   = models.CharField(max_length=15, null=True, blank=True)
    fax                    = models.CharField(max_length=13, null=True, blank=True)
    email                  = models.EmailField(max_length=100, null=True, blank=True)
    status                 = models.CharField(max_length=30, null=True, blank=True)
    tipo                   = models.CharField(max_length=30, null=True, blank=True)
    site               = models.CharField(max_length=255, null=True, blank=True)     
    
    def __str__(self):
        return "%s" % (self.nome)

    