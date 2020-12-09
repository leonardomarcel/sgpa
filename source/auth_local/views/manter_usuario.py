from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from auth_local.models.usuario_orgao import UsuarioOrgao
from auth_local.models.perfil import Perfil
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from passagem.forms.usuario_buscar_form import UsuarioBuscarForm
from passagem.forms.gestor_password_form import GestorPasswordForm
from passagem.forms.gestor_form import GestorForm
from util.util import get_gestor_by_id, is_meu_perfil_gestor_form_changed
from basico.models.orgao import Orgao
from django.core.paginator import Paginator
from util.group_required_mixin import GroupRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import TemplateView
from util.util import is_recaptcha_success


class UsuarioListView(GroupRequiredMixin, ListView):
    model = UsuarioOrgao
    form_class = UsuarioBuscarForm
    template_name = "usuario/listagem.html"
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = self.get_queryset().distinct()
        
        context['buscar_form'] = self.form_class(self.request.GET)
        context['usuarios'] = usuarios
        context['total_usuarios'] = usuarios.count()
        page = int(self.request.GET.get('usuarios_page', 1))
        context['usuarios_paginator'] = Paginator(usuarios, 10).page(page)
        return context
    
    def get_queryset(self):
        request = self.request.GET
        buscar_form = self.form_class(self.request.GET)
        gestor = get_gestor_by_id(self.request.user.id)
        
        if gestor.is_gestor_amgesp():
            usuarios = super(UsuarioListView, self).get_queryset().all().order_by('nome')
        else:
            usuarios = super(UsuarioListView, self).get_queryset().filter(orgao=gestor.orgao).distinct().order_by('nome')
        
        if buscar_form.is_valid():
            nome = request.get('nome')
            id_ouvidoria = request.get('ouvidoria')
            id_perfil = request.get('perfil')
            status = request.get('status')
            cpf = request.get('cpf')

            if cpf:
                usuarios = usuarios.filter(Q(cpf__icontains=cpf))
            if nome:
                usuarios = usuarios.filter(Q(nome__icontains=nome))
                
            if id_ouvidoria:
                usuarios = usuarios.filter(Q(orgao__id=id_ouvidoria))
            
            if id_perfil:
                usuarios = usuarios.filter(Q(perfil__id=id_perfil))

            if status:
                if status != 'T': 
                    is_active = (status == 'A')
                    usuarios = usuarios.filter(Q(is_active=is_active))
       
        return usuarios

class UsuarioCreateView(GroupRequiredMixin, CreateView):
    model = UsuarioOrgao
    form_class = GestorForm
    template_name = "usuario/formulario.html"
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]
    
    @method_decorator(login_required)
    def get(self, request):
        usuario_form = self.form_class(use_required_attribute=False)

        return render(request, self.template_name, context=locals())
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        usuario_form = self.form_class(request.POST, use_required_attribute=False)
        if usuario_form.is_valid():
            orgao_amgesp = Orgao.objects.get(sigla='amgesp')
            orgao = usuario_form.cleaned_data.get('orgao')
            usuario = usuario_form.save(commit=False)
            usuario.orgao = orgao
            usuario.email = usuario.email.lower()
            usuario.is_active = True
            usuario.save()
            perfil_gestor = Perfil.ID_GESTOR_AMGESP
            if usuario.orgao == orgao_amgesp and usuario.perfil.id == perfil_gestor:
                group_gestor_amgesp = Group.objects.get(name=UsuarioOrgao.GROUP_GESTOR_AMGESP)
                group_gestor_amgesp.user_set.add(usuario)
            
            messages.success(request, '<strong>' + usuario.nome + '</strong> foi salvo com sucesso. E-mail com senha enviado para <strong>' + usuario.email + '</strong>')
            return redirect(reverse('auth_local:listar_usuarios'))
        
      
        return render(request, self.template_name, context=locals())

class UsuarioUpdateView(GroupRequiredMixin, UpdateView):
    model = UsuarioOrgao 
    form_class = GestorForm
    template_name = "usuario/formulario.html"
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]
    
    @method_decorator(login_required)
    def get(self, request, id_usuario):
        usuario_orgao = get_object_or_404(UsuarioOrgao, pk=id_usuario)
        gestor_logado = get_gestor_by_id(self.request.user.id)
        
        print (gestor_logado.is_gestor_passagem())
        if not gestor_logado.is_gestor_amgesp()  and not gestor_logado.is_superuser:
            messages.error(request, 'Você não possui permissão para visualizar informações desse usuário.')
            return redirect(reverse('auth_local:listar_usuarios'))
        usuario_form = self.form_class(instance=usuario_orgao)
        return render(request, self.template_name, context=locals())
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        id_usuario = kwargs['id_usuario']
        usuario_orgao = get_object_or_404(UsuarioOrgao, pk = id_usuario)
        usuario_form = self.form_class(request.POST, instance=usuario_orgao)
        
        gestor_logado = get_gestor_by_id(self.request.user.id)
        
        if not gestor_logado.is_gestor_amgesp()  and not gestor_logado.is_superuser:
            messages.error(request, 'Você não possui permissão para alterar dados desse usuário.')
            return redirect(reverse('listar_usuarios'))
        
        if usuario_form.is_valid():
            usuario_orgao = usuario_form.save(commit=False)
            usuario_orgao.is_active = True
                
            usuario_orgao.orgao = usuario_form.cleaned_data.get('orgao')
            usuario_orgao.save()
            usuario_orgao.groups.clear()

            
            perfil_gestor = Perfil.ID_GESTOR_AMGESP
            orgao_amgesp = Orgao.objects.get(sigla='amgesp')

            if usuario_orgao.orgao == orgao_amgesp and usuario_orgao.perfil.id == perfil_gestor:
                group_gestor_amgesp = Group.objects.get(name=UsuarioOrgao.GROUP_GESTOR_AMGESP)
                group_gestor_amgesp.user_set.add(usuario_orgao)
            
            messages.success(request, '<strong>' + usuario_orgao.nome + '</strong> foi atualizado com sucesso. ')
            return redirect(reverse('auth_local:listar_usuarios'))
        
        return render(request, self.template_name, context=locals())

class MeuPerfilView(GroupRequiredMixin, UpdateView):
    template_name = "usuario/meu_perfil.html"
    model = UsuarioOrgao
    form_class = GestorPasswordForm
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    @method_decorator(login_required)
    def get(self, request):
        usuario = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        meu_perfil_form = self.form_class(usuario=usuario)
        
        return render(request, self.template_name, context=locals())
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        usuario = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        meu_perfil_form = self.form_class(request.POST, usuario=usuario)

        if not is_meu_perfil_gestor_form_changed(meu_perfil_form):
            messages.warning(request, 'Nenhuma alteração feita.')
        
        if meu_perfil_form.is_valid():
            nome = meu_perfil_form.cleaned_data.get('nome')
            nova_senha = meu_perfil_form.cleaned_data.get('nova_senha')
            telefone = meu_perfil_form.cleaned_data.get('telefone')
            
            if usuario.telefone != telefone:
                usuario.telefone = telefone 
                
            if nova_senha:
                usuario.set_password(nova_senha)
            
            if usuario.nome != nome:
                usuario.nome = nome
                
            usuario.save()
            messages.success(request, '<strong>' + usuario.nome + '</strong> informações atualizadas com sucesso. ')
        
        return render(request, self.template_name, context=locals())
    
class UsuarioDeleteView(GroupRequiredMixin, DeleteView):
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    @method_decorator(login_required)
    def get(self, request, id_usuario):
        usuario_logado = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        usuario_orgao = get_object_or_404(UsuarioOrgao, pk=id_usuario)
        
        if usuario_orgao:
            usuario_orgao.is_active = False
            usuario_orgao.save()
            messages.success(request, '<strong>' + usuario_orgao.nome + '</strong> foi desativado com sucesso. ')
            return redirect(reverse('listar_usuarios'))

        return render(request, self.template_name, context=locals())

class EsqueceuSuaSenhaGestorView(TemplateView):
    template_name = "esqueceu_sua_senha_gestor.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        #recaptcha_response = request.POST.get('g-recaptcha-response')
        
        #if is_recaptcha_success(recaptcha_response):
        cpf = request.POST.get('cpf_redefinicao')
        
        if not cpf:
            messages.error(request, 'É obrigatório informar o Login (CPF).')
            return render(request, self.template_name)
        else:
            try:
                gestor = UsuarioOrgao.objects.get(cpf=cpf)
                gestor.save_new_password_generate()
                
                username = gestor.email.split('@')[0]
                username = username[:3]
                domain = gestor.email.split('@')[1]
                email = username + '*****@'+ domain

                messages.success(request, 'Uma nova senha foi enviada para <strong>' + email + '</strong>')
            except UsuarioOrgao.DoesNotExist:
                gestor = None
                messages.error(request, 'Não foi encontrado nenhum usuário com o CPF informado.')
                return render(request, self.template_name)
        #else:
            #messages.error(request, 'É obrigatório marcar o <strong>reCAPTCHA</strong>.')
            #return render(request, self.template_name)
        
        return redirect('login')        