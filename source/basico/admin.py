from django.contrib import admin

from basico.models.municipio import Municipio
from basico.models.pais import Pais
from basico.models.orgao import Orgao

admin.site.register(Municipio)
admin.site.register(Pais)
admin.site.register(Orgao)
