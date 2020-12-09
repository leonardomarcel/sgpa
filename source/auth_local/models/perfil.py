from reversion import revisions as reversion
from django.db import models

@reversion.register()
class Perfil(models.Model):
    ID_GESTOR_PASSAGEM = 1
    ID_GESTOR_AMGESP = 2
    ID_AGENCIA_VIAGEM = 3
    

    nome = models.CharField('Nome do Perfil', max_length=100, null=False, blank=False)
    
    def is_gestor_passagem(self):
        return self.pk == self.ID_GESTOR_PASSAGEM
    
    def is_gestor_amgesp(self):
        return self.pk == self.ID_GESTOR_AMGESP
    
    def is_agencia_viagem(self):
        return self.pk == self.ID_AGENCIA_VIAGEM
    
    def __str__(self):
        return "%s" % (self.nome)
    
    class Meta:
        app_label = 'auth_local'
        db_table =  app_label + '_perfil'
        default_related_name = 'perfil'