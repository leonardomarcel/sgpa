from django.db import models
from util.fields import CharUpperField
from django.apps import apps
from datetime import date
import os
from django.conf import settings




def anexo_processo(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    extensao = filename.split('.')[-1]
    solicitacao_passagem = apps.get_model('passagem', 'SolicitacaoPassagem')
    solicitacao_passagem = solicitacao_passagem.objects.last()
    if not solicitacao_passagem:
        solicitacao_passagem = 1
        
    file_name =  'arquivos_processo/'+str(solicitacao_passagem.id)+'/{}.{}'.format(instance.nome, extensao)
    fullname = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return file_name

class AnexoProcessoSolicitacaoPassagem(models.Model):

    arquivo  = models.FileField(upload_to=anexo_processo, null=True,blank=True)
    nome = CharUpperField('Nome', max_length=200, null=True, blank=True)
    tamanho = CharUpperField('Tamanho', max_length=200, null=True, blank=True) 
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    
