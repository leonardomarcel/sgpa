import os

from django.apps import apps
from django.conf import settings
from django.db import models
import reversion

from basico.models.orgao import Orgao
from passagem.model.motivo import Motivo
from auth_local.models.usuario_orgao import UsuarioOrgao
from datetime import datetime
from passagem.model.passagem import Passagem
from passagem.model.anexo_processo_solicitacao_passagem import AnexoProcessoSolicitacaoPassagem




VIAGEM_SERVICO_CHOICE = (
                 ('S','SIM'),
                 ('N','NÃO'),
                 )

STATUS_CHOICE = (
                 ('ABERTA','ABERTA'),
                 ('COM PENDENCIA','COM PENDENCIA'),
                 ('AUTORIZADA','AUTORIZADA'),
                 )

def anexo_diario(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if  instance.pk:
        instance = SolicitacaoPassagem.objects.last().pk
    else:
        instance = SolicitacaoPassagem.objects.last()
        if not instance:
            instance = 1
        else:
            instance = instance.id + 1
    file_name =  'arquivos_diario/{0}.{2}'.format(instance, datetime.now(),
                                          filename.split('.')[-1])
    fullname = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return file_name

def anexo_evento(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if  instance.pk:
        instance = SolicitacaoPassagem.objects.last().pk
    else:
        instance = SolicitacaoPassagem.objects.last()
        if not instance:
            instance = 1
        else:
            instance = instance.id + 1
    file_name =  'arquivos_evento/{0}.{2}'.format(instance, datetime.now(),
                                          filename.split('.')[-1])
    fullname = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return file_name



@reversion.register()
class SolicitacaoPassagem(models.Model):

    codigo                 = models.CharField(max_length=10, null=True,blank=True)
    cadastro_concluido     = models.BooleanField(default=False)
    data                   = models.DateField(null=True,blank=True)
    usuario                = models.ForeignKey(UsuarioOrgao, on_delete=models.CASCADE, null=True,blank=True)
    orgao                  = models.ForeignKey(Orgao, on_delete=models.CASCADE)
    motivo                 = models.ForeignKey(Motivo, on_delete=models.CASCADE)
    viagem_servico         = models.CharField(choices=VIAGEM_SERVICO_CHOICE, max_length=100)
    descricao_evento       = models.TextField('Descrição do Evento', null=True,blank=True)
    anexo_evento           = models.FileField(upload_to=anexo_evento, null=True,blank=True)
    anexos_processo       = models.ManyToManyField(AnexoProcessoSolicitacaoPassagem, null=True,blank=True) 
    anexo_diario           = models.FileField(upload_to=anexo_diario, null=True,blank=True)
    nota_empenho           = models.FileField(null=True,blank=True)
    fonte_recurso          = models.TextField(null=True,blank=True)
    unidade_gestora        = models.TextField(null=True,blank=True)
    status                 = models.CharField(choices=STATUS_CHOICE, max_length=100)
    passagens              = models.ManyToManyField(Passagem) 
    urgente                = models.BooleanField(null=True,blank=True, default=False)
    justificativa_urgencia = models.TextField('Justificativa da Urgência',null=True,blank=True) 
    
    
    def __str__(self):
        return "%s" % (self.id)

    
    def tem_passageiro_passagem(self):
        return apps.get_model('passagem.PassageiroPassagem').objects.filter(passagem__in=self.passagens.all().values_list('pk')).exists()