from datetime import timedelta
import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone


import reversion

@reversion.register()
class Token(models.Model):
    hash = models.CharField(verbose_name="Hash", max_length=500)
    data_expiracao = models.DateTimeField(verbose_name="Data de Expiração")
    is_usado = models.BooleanField(verbose_name="Usado?", default=False)

    def gerar_hash(self, usuario):
        token_str = usuario.email
        token_str += usuario.password
        token_str += timezone.now().isoformat()
        encoder = hashlib.md5()
        encoder.update(token_str.encode('utf-8'))
        self.hash = encoder.hexdigest()

        return self.hash

    def get_data_expiracao(self):
        now = timezone.now()
        self.data_expiracao = now + timedelta(days=settings.TOKEN_VALIDITY)
        return self.data_expiracao

    #def __str__(self):
        #return '%s - %s - %s' % (self.usuario.email, self.data_expiracao, self.is_usado)

    class Meta:
        app_label = 'auth_local'
