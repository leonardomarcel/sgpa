from django.db import models
from util.fields import CharUpperField

import reversion

@reversion.register()
class Orgao(models.Model):
    
    descricao = CharUpperField('Razão Social', max_length=101)
    sigla = CharUpperField('Sigla', max_length=25, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    
    def is_amgesp(self):
        return self.sigla == 'amgesp'
    
    def get_nome_orgao(self):
        if self.sigla:
            return '%s - %s' % (self.sigla, self.descricao)
        
        return '%s' % self.descricao
    
    def __str__(self):
        if not self.sigla:
            return '%s' % self.descricao
        
        return '%s - %s' % (self.sigla, self.descricao)
    
    class Meta:
        app_label = 'basico'
        verbose_name = 'Órgão'
        verbose_name_plural = 'Órgãos'
        '''
        permissions = (
            ("view_orgao", "Ver órgãos"),
        )
        '''
