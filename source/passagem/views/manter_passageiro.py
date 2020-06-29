from util.group_required_mixin import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from passagem.model.passageiro import Passageiro
from passagem.forms.passageiro_form import PassageiroForm, PassageiroBuscarForm
from basico.models.orgao import Orgao
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.db.models import Q


class PassageiroCreateView(GroupRequiredMixin, CreateView):
    model = Passageiro
    form_class = PassageiroForm
    template_name = 'passageiro/editar_passageiro.html'
    
    @method_decorator(login_required)
    def get(self, request):
        passageiro_form = self.form_class(use_required_attribute=False)
        
        return render(request, self.template_name, context=locals())
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        passageiro_form = self.form_class(request.POST)
        if passageiro_form.is_valid():
            passageiro = passageiro_form.save()
            messages.success(request, '<strong> Passageiro(a)' + passageiro.nome + '</strong> foi salvo(a) com sucesso. <strong>')
            return HttpResponseRedirect(reverse('passagem:passageiros'))
        return render(request, self.template_name, context=locals())  
    

class PassageiroListView(GroupRequiredMixin, ListView):
    model      = Passageiro
    form_class = PassageiroBuscarForm
    template_name   = "passageiro/passageiros_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        passageiros = self.get_queryset().distinct()
        context['buscar_form'] = self.form_class(self.request.GET)
        context['passageiros'] = passageiros
        page = int(self.request.GET.get('passageiros_page', 1))
        context['passageiro_paginator'] = Paginator(passageiros, 10).page(page)
        return context
    
    def get_queryset(self):
        passageiros = super(PassageiroListView, self).get_queryset().all()
        request = self.request.GET
        buscar_form = self.form_class(self.request.GET)
        if buscar_form.is_valid:
            cpf=request.get('cpf')
            nome=request.get('nome')
            if cpf:
                passageiros = passageiros.filter(Q(cpf__icontains=cpf))
            if nome:
                passageiros = passageiros.filter(Q(nome__icontains=nome))
        return passageiros
    
class PassageiroUpdateView(GroupRequiredMixin, UpdateView):
    model = Passageiro
    form_class = PassageiroForm
    template_name = 'passageiro/editar_passageiro.html'
    
    @method_decorator(login_required)
    def get(self, request, id_passageiro):
        passageiro = get_object_or_404(Passageiro, pk=id_passageiro)
        passageiro_form = self.form_class(instance=passageiro)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        id_passageiro = kwargs['id_passageiro']
        passageiro = get_object_or_404(Passageiro, pk=id_passageiro)
        passageiro_form = self.form_class(request.POST, instance=passageiro)
        if passageiro_form.is_valid():
            passageiro_form.save()
            messages.success(request, '<strong> Passageiro(a) editado com sucesso!')
            return HttpResponseRedirect(reverse('passagem:passageiros'))
        return render(request, self.template_name, context=locals())
        