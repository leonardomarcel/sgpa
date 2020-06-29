from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_local.models.usuario_orgao import UsuarioOrgao
#from auth_local.base.models.usuario_base import UsuarioBase


class UserModelAdmin(UserAdmin):


    list_display = ('email', 'is_superuser', 'is_active')
    list_filter = ('is_superuser',)
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'email', 'foto', 'telefone',)}),
        ('Permissão', {
            'fields': (('is_active'), ('is_superuser',),
                       ('user_permissions',), ('groups'))}),

        ('Datas Importantes', {
            'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'senha1', 'senha2')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(UsuarioOrgao, UserModelAdmin)