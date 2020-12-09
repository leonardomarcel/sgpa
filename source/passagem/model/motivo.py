from django.db import models
import reversion


@reversion.register()
class Motivo(models.Model):
    
 
    nome = models.CharField(max_length=100)
    
    
    def __str__(self):
        return "%s" % (self.nome)

    