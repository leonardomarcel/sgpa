# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
# from django.db import models
# from reversion import revisions as reversion
# from auth_local.models.usuario_manager import UsuarioManager
# 
# from auth_local.util.util import mkpass
# from util.fields import CharUpperField
# import datetime
# from auth_local.models.perfil import Perfil
# from django.apps import apps
# from auth_local.util.email import enviar_email_nova_senha_gestor,\
#     enviar_email_nova_senha_cidadao
# 
# def name_foto_perfil_usuario(instance, filename):
#     extension = filename.split('.')[-1]
#     data = datetime.datetime.now().strftime("%H_%M_%S")
#     if instance.pk:
#         return 'profile/FOTO_{}_{}.{}'.format(instance.get_short_name(), data, extension)
#     else:
#         return 'profile/FOTO_{}.{}'.format('PERFIL', extension)
# 
# @reversion.register()
# class UsuarioBase(AbstractBaseUser, PermissionsMixin):
#     """ 
#         Todas as modificações de usuário devem ser feitas no modelo Usuario, nunca em UsuarioBase.
#         As modificações realizadas aqui são para efeito do projeto base.
#     """
#     GROUP_GESTOR_PASSAGEM = "GESTOR_PASSAGEM"
#     GROUP_GESTOR_AMGESP = "GESTOR_AMGESP"
#     GROUP_AGENCIA_VIAGEM = "AGENCIA_VIAGEM"
# 
#     objects = UsuarioManager()
#     nome = CharUpperField('Nome', max_length=100, null=False, blank=False)
#     email = models.EmailField(verbose_name='Endereço de Email', max_length=255, unique=True, db_index=True)
#     
#     foto = models.ImageField('Foto de Perfil', upload_to=name_foto_perfil_usuario, null=True, blank=True)
#     telefone = models.CharField(verbose_name='Telefone', max_length=20, null=True, blank=True)
#     
#     is_active = models.BooleanField(verbose_name='Ativo?', default=True)
#     is_first_login = models.BooleanField(verbose_name='Primeiro Login?', default = False)
#     
#     perfil = models.ForeignKey(Perfil, verbose_name='Perfil', related_name='usuario_perfil', null=True, blank=True, on_delete=models.PROTECT)
#     
#     USERNAME_FIELD = 'email'
#     
#     def is_gestor_passagem(self):
#         return self.perfil.is_gestor_passagem()
#     
#     def is_gestor_amgesp(self):
#         return self.perfil.is_gestor_amgesp()
#     
#     def is_agencia_viagem(self):
#         return self.perfil.is_agencia_viagem()
#     
#     
#     
#     
#    
#     
#     def get_full_name(self):
#         if self.nome:
#             return self.nome
#         return self.email
# 
#     def get_short_name(self):
#         if self.nome:
#             palavras = self.nome.split()
#             return palavras[0] + " " + palavras[len(palavras)-1]
#         return self.email.split()
# 
#     def has_group(self, group_name):
#         group =  Group.objects.get(name=group_name) 
#         return group in self.groups.all()
# 
#     def __unicode__(self):
#         if self.nome:
#             return self.nome
#         return self.email
# 
#     @property
#     def is_staff(self):
#         return self.is_superuser
#     
#     def save_new_password_generate(self, *args, **kwargs):
#         self.gerar_nova_senha()
#         super(UsuarioBase, self).save(*args, **kwargs)
        
#     def save(self, *args, **kwargs):
#         if not self.pk and not self.password:
#             self.gerar_nova_senha()
#         super(UsuarioBase, self).save(*args, **kwargs)
    
#     def gerar_nova_senha(self):
#         nova_senha = mkpass(8)
#         self.set_password(nova_senha)
#         #if self.is_usuario_orgao():
#         enviar_email_nova_senha_gestor(self, nova_senha)
#         
              
#        return nova_senha
    
#     def __str__(self):
#         return self.get_full_name()
# 
#     class Meta:
#         app_label = 'auth_local'
#         db_table =  app_label + '_usuario_base'
#         default_related_name = 'usuario_base'