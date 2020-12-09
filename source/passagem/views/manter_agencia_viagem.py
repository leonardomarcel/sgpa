from util.group_required_mixin import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from passagem.forms.agencia_viagem_form import AgenciaViagemForm
from passagem.model.agencia import Agencia
from auth_local.models.usuario_orgao import UsuarioOrgao

class AgenciaViagemCreateView(GroupRequiredMixin, CreateView):
    model          = Agencia
    form_class     = AgenciaViagemForm  
    template_name  = 'agencia/editar_agencia_viagem.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get(self, request):
        agencia_viagem_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())

    def post(self, request, *args, **kwargs):
        agencia_viagem_form = self.form_class(request.POST)
        if agencia_viagem_form.is_valid():
            agencia_viagem_form.save()
            messages.success(request, '<strong> Agencia de viagem salvo com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:agencias_viagem'))
        else:
            print(agencia_viagem_form.errors)
        
        return render(request, self.template_name, context=locals())

class AgenciaViagemListView(GroupRequiredMixin, ListView):
    model    = Agencia
    template_name = 'agencia/agencia_viagem_list.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agencias = self.get_queryset().distinct()
        context['agencias'] = agencias
        page = int(self.request.GET.get('agencias_page', 1))
        context['agencia_paginator'] = Paginator(agencias, 10).page(page)
        return context

class AgenciaViagemUpdateView(GroupRequiredMixin, UpdateView):
    model = Agencia
    form_class = AgenciaViagemForm
    template_name = 'agencia/editar_agencia_viagem.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get(self, request, id_agencia_viagem):
        agencia_viagem       = get_object_or_404(Agencia, pk=id_agencia_viagem)
        agencia_viagem_form  = self.form_class(instance=agencia_viagem)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        id_agencia_viagem   = kwargs['id_agencia_viagem']
        agencia_viagem      = get_object_or_404(Agencia, pk=id_agencia_viagem)
        agencia_viagem_form = self.form_class(request.POST, instance=agencia_viagem)
        if agencia_viagem_form.is_valid():
            agencia_viagem_form.save() 
            messages.success(request, '<strong> Agencia de viagem salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:agencias_viagem'))