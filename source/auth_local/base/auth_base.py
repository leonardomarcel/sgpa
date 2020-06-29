from django.contrib import auth as django_auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.db.models.aggregates import Count
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from auth_local.models.token import Token

class AuthBase():
    """
        Não modifique esta classe, ao menos que você esteja editando o projeto base!
        Modificações nas defs de autenticação devem ser feitas no auth_local.py.
    """
    @login_required
    def index(request):
        try: 
            pass                
        except Exception as e:
            messages.error(request, e)
            
        return render(request, 'index.html', context=locals())

    @login_required
    def logout(request,):
        """."""
        django_auth.logout(request)
        return redirect('login')

    def confirmar_nova_senha(request):
        if 'token' in request.GET.keys():
            token = get_object_or_404(Token, hash=request.GET['token'], is_usado=False)

            if token.data_expiracao >= timezone.now():
                token.is_usado = True
                token.save()

                if token.usuario.is_active:
                    token.usuario.gerar_nova_senha()
                    token.usuario.save()
                    messages.success(request, "Uma nova senha foi enviada para seu email.")
                else:
                    messages.error(request, "Conta inativa. Entre em contato com o administrador.")
            else:
                messages.error(request, "Token expirado! Solicite novamente.")

        return redirect(request, 'login', context=locals())


    def cancelar_nova_senha(request):
        if 'token' in request.GET.keys():
            token = get_object_or_404(Token,
                                    hash=request.GET['token'],
                                    is_usado=False)
            token.is_usado = False
            token.save()
            messages.success(request, "Solicitação de nova senha cancelada.")
        return redirect(request, 'login')


    @login_required
    @permission_required('auth_local.change_usuario')
    def editar_usuario(request, id_usuario=None):
        
        if Group.objects.count() ==  0:
            messages.error(request, 'É necessário criar os grupos de permissões para o sistema')   
            return redirect(reverse('listar_usuarios'))
        
        if id_usuario:
            usuario = get_object_or_404(Usuario, pk=id_usuario)
            
        else:
            usuario = Usuario()
            usuario.is_active = True
            usuario.is_superuser = False
            
        if request.method == "POST":
            usuario_form = UsuarioForm(request.POST, request.FILES, instance=usuario)

            if usuario_form.is_valid():
                try:
                    usuario = usuario_form.save()
                    
                    if id_usuario:
                        messages.success(request, usuario.nome + ' atualizado com sucesso')
                    else:
                        messages.success(request, usuario.nome + ' cadastrado com sucesso')

                    return redirect(reverse('listar_usuarios'))
                except Exception as e:
                    messages.error(request, 'Ocorreu um problema ao tentar salvar este usuário. ' + str(e))
        else:
            usuario_form = UsuarioForm(instance=usuario)
        return render(request, 'editar_usuario.html' , context=locals())

    @login_required
    @permission_required('auth_local.delete_usuario')
    def excluir_usuario(request, id_usuario):
        usuario = get_object_or_404(Usuario, pk=id_usuario)
        try:
            usuario.delete()
            messages.success(request,  usuario.nome + ' removido com sucesso.')
        except:
            messages.error(request, 'Existem associações em ' + usuario.nome + ', não é possível remover este usuário.')
            return redirect(reverse('editar_usuario',  args=[id_usuario]))
        
        return redirect(reverse('listar_usuarios'))

    @login_required
    @permission_required('auth_local.view_usuarios')
    def listar_usuarios(request):
        usuarios = Usuario.objects.filter(is_active=True).order_by('nome')
        pesquisa = request.GET.get('pesquisa', '')

        if pesquisa:
            usuarios = usuarios.filter(Q(nome__icontains=pesquisa)
                                    | Q(telefone__icontains=pesquisa)
                                    | Q(email__icontains=pesquisa))

        return render(request, 'listar_usuarios.html', context=locals())