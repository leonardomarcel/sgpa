from django.contrib import auth as django_auth
from auth_local.base.auth_base import AuthBase
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http.response import HttpResponse
from auth_local.models.usuario_orgao import UsuarioOrgao

class AuthLocal(AuthBase):
    
    def login(request):
        user = request.user
        redirect_to = request.GET.get('next', 'passagem')
        

        if user.id:
            return redirect('passagem')
        
        if request.POST:
            try:
                cpf = request.POST.get('cpf')
                usuario_orgao = UsuarioOrgao.objects.get(cpf=cpf)
                senha = request.POST.get('senha')
                email = usuario_orgao.email
                usuario = django_auth.authenticate(email=email, password=senha)

                if usuario is not None:
                    if usuario.is_active:
                        django_auth.login(request, usuario)
                        gestor = UsuarioOrgao.objects.get(cpf=cpf)
                        return redirect('passagem')
                    else:
                        messages.error(request, 'Usuário desativado.')
                else:
                    messages.error(request, 'Usuário e/ou senha inválido(s).')
            except:
                messages.error(request, 'Ocorreu um erro ao tentar fazer login.')
                return render(request,  'login.html', context=locals())
                
        return render(request,  'login.html', context=locals())
    
    
    
    @login_required
    def logout(request,):
        django_auth.logout(request)
        return redirect('login')
    
    
    @login_required
    def alterar_senha(request):
        u"""."""
        form = AlterarSenhaForm(request.POST or None, usuario=request.user)
    
        if request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Senha alterada com sucesso.')
                request.user.is_first_login = False
                request.user.save()
                return redirect('index')
    
        return render_to_response('alterar_senha.html', locals(),
                                  context_instance=RequestContext(request))
    
    
    def esqueceu_senha(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            usuario = get_object_or_404(Usuario, email=email)
    
            if usuario.is_active:
                token = Token()
                token.gerar_hash(usuario)
                token.get_data_expiracao()
                token.is_usado = False
                token.usuario = usuario
                token.save()
                enviar_confirmacao_nova_senha(usuario, token)
                messages.success(request, u"Acesse seu email e siga os passos necessários.")
            else:
                messages.error(request, u"Conta inativa. Entre em contato com o administrador.")
    
        return render_to_response('esqueceu_senha.html',
                                  locals(), context_instance=RequestContext(request))
    
    
    def confirmar_nova_senha(request):
        if u'token' in request.GET.keys():
            token = get_object_or_404(Token,
                                      hash=request.GET['token'],
                                      is_usado=False)
    
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
                messages.error(request, u"Token expirado! Solicite novamente.")
    
        return redirect('login')
    
    
    def cancelar_nova_senha(request):
        if u'token' in request.GET.keys():
            token = get_object_or_404(Token,
                                      hash=request.GET['token'],
                                      is_usado=False)
            token.is_usado = False
            token.save()
            messages.success(request, u"Solicitação de nova senha cancelada.")
        return redirect('login')
    
        