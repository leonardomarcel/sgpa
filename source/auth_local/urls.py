from django.conf.urls import url
from django.urls import path


from auth_local.views.manter_usuario import UsuarioListView, UsuarioUpdateView, UsuarioCreateView, UsuarioDeleteView,\
    MeuPerfilView, EsqueceuSuaSenhaGestorView


from django.contrib.auth.decorators import login_required
app_name = 'auth_local' 

urlpatterns = [
    
    
    
    path('usuarios/meu_perfil/', MeuPerfilView.as_view(), name="meu_perfil"),
    path('usuarios/', login_required(UsuarioListView.as_view()), name="listar_usuarios"),
    path('usuarios/cadastrar/', UsuarioCreateView.as_view(), name="cadastrar_usuario"),
    path('usuarios/editar/<int:id_usuario>/', UsuarioUpdateView.as_view(), name="editar_usuario"),
    path('usuarios/remover/<int:id_usuario>/', UsuarioDeleteView.as_view(), name="remover_usuario"),
    path('esqueceu-senha/', EsqueceuSuaSenhaGestorView.as_view(), name="gestor_esqueceu_sua_senha"),
    
   
]