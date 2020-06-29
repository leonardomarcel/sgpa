from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from reversion import revisions as reversion
import datetime
from django.db import models
from auth_local.util.util import mkpass
from util.fields import CharUpperField
from auth_local.models.usuario_manager import UsuarioManager
from basico.models.orgao import Orgao
from auth_local.models.perfil import Perfil
from auth_local.util.email import enviar_email_nova_senha_gestor

def name_foto_perfil_usuario(instance, filename):
    extension = filename.split('.')[-1]
    data = datetime.datetime.now().strftime("%H_%M_%S")
    if instance.pk:
        return 'profile/FOTO_{}_{}.{}'.format(instance.get_short_name(), data, extension)
    else:
        return 'profile/FOTO_{}.{}'.format('PERFIL', extension)

@reversion.register()
class UsuarioOrgao(AbstractBaseUser, PermissionsMixin):
    """ Todas as modificações de usuário devem ser feitas neste modelo, nunca em UsuarioBase. """
    
    objects = UsuarioManager()
    cpf = models.CharField('CPF do Usuário', max_length=14, null=False, blank=False)
    orgao = models.ForeignKey(Orgao, verbose_name='Órgão', related_name='usuario_orgao', on_delete=models.PROTECT)
    
    
    
    GROUP_GESTOR_PASSAGEM = "GESTOR_PASSAGEM"
    GROUP_GESTOR_AMGESP = "GESTOR_AMGESP"
    GROUP_AGENCIA_VIAGEM = "AGENCIA_VIAGEM"

    objects = UsuarioManager()
    nome = CharUpperField('Nome', max_length=100, null=False, blank=False)
    email = models.EmailField(verbose_name='Endereço de Email', max_length=255, unique=True, db_index=True)
    
    foto = models.ImageField('Foto de Perfil', upload_to=name_foto_perfil_usuario, null=True, blank=True)
    telefone = models.CharField(verbose_name='Telefone', max_length=20, null=True, blank=True)
    
    is_active = models.BooleanField(verbose_name='Ativo?', default=True)
    is_first_login = models.BooleanField(verbose_name='Primeiro Login?', default = False)
    
    perfil = models.ForeignKey(Perfil, verbose_name='Perfil', related_name='usuario_perfil', null=True, blank=True, on_delete=models.PROTECT)
    
    USERNAME_FIELD = 'email'

    def is_gestor_passagem(self):
        return self.perfil.is_gestor_passagem()
    
    def is_gestor_amgesp(self):
        return self.perfil.is_gestor_amgesp()
    
    def is_agencia_viagem(self):
        return self.perfil.is_agencia_viagem()
    
    def get_full_name(self):
        if self.nome:
            return self.nome
        return self.email

    def get_short_name(self):
        if self.nome:
            palavras = self.nome.split()
            return palavras[0] + " " + palavras[len(palavras)-1]
        return self.email.split()

    def has_group(self, group_name):
        group =  Group.objects.get(name=group_name) 
        return group in self.groups.all()

    def __unicode__(self):
        if self.nome:
            return self.nome
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser
    
    def save_new_password_generate(self, *args, **kwargs):
        self.gerar_nova_senha()
        super(UsuarioOrgao, self).save(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            self.gerar_nova_senha()
        super(UsuarioOrgao, self).save(*args, **kwargs)
     
    def gerar_nova_senha(self):
        nova_senha = mkpass(8)
        self.set_password(nova_senha)
        enviar_email_nova_senha_gestor(self, nova_senha)
        #if self.is_usuario_orgao():
                
        return nova_senha
     
#     def __str__(self):
#         return self.get_full_name()

    def __str__(self):
        return "%s - %s" % (self.cpf, self.nome) 
    
    
    
    
    
    

#     def save(self, *args, **kwargs):
#         if not self.pk and not self.password:
#             self.gerar_nova_senha()
#         super(UsuarioOrgao, self).save(*args, **kwargs)
        
        
#     def gerar_senha_hash(self):
#         nova_senha = mkpass(16)
#         self.set_password(nova_senha)
#         return nova_senha
        
    class Meta:
        app_label = 'auth_local'
        db_table =  app_label + '_usuario_orgao'
        default_related_name = 'usuario_orgao'
#         permissions = (
#             ("view_painel", "Acesso ao passagem"),
#             ("cge", "Gestores da CGE"),
#             ("add_gestor", "Adicionar novos gestores"),
#             ("view_usuarios", "Visualizar usuários"),
#             ("view_cidadaos", "Visualizar Cidadãos"),
#             ("forgot_password", "Adicionar novos gestores"),
#         )