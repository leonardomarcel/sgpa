from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Os usuários devem ter um endereço de e-mail')

        usuario = self.model(
            email=UsuarioManager.normalize_email(email),
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password):
        usuario = self.create_user(email, password=password)
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


    def usuarios_orgao(self, user):
        return super(UsuarioManager, self).get_queryset().filter(orgao=user.orgao)