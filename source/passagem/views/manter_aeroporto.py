
from util.group_required_mixin import GroupRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from passagem.model.aeroporto import Aeroporto
from passagem.forms.aeroporto_form import AeroportoForm
from auth_local.models.usuario_orgao import UsuarioOrgao

class AeroportoCreateView(GroupRequiredMixin, CreateView):
    model           = Aeroporto
    form_class      = AeroportoForm
    template_name   = 'aeroporto/editar_aeroporto.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    @method_decorator(login_required)
    def get(self, request):
        aeroporto_form = self.form_class(use_required_attribute=False)

        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        aeroporto_form = self.form_class(request.POST)
        if aeroporto_form.is_valid():
            aeroporto_form.save()
            messages.success(request, '<strong> Aeroporto salvo com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:aeroportos'))
        
        return render(request, self.template_name, context=locals())

class AeroportoListView(GroupRequiredMixin, ListView):
    model = Aeroporto
    template_name = 'aeroporto/aeroporto_list.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    #@method_decorator(login_required)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aeroportos = self.get_queryset().distinct()
        context['aeroportos'] = aeroportos
        page = int(self.request.GET.get('aeroportos_page', 1))
        context['aeroporto_paginator'] = Paginator(aeroportos, 10).page(page)
        return context

class AeroportoUpdateView(GroupRequiredMixin, UpdateView):
    model = Aeroporto
    form_class = AeroportoForm
    template_name = 'aeroporto/editar_aeroporto.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    #@method_decorator(login_required)
    def get(self, request, id_aeroporto):
        aeroporto       = get_object_or_404(Aeroporto, pk=id_aeroporto)
        aeroporto_form  = self.form_class(instance=aeroporto)
        return render(request, self.template_name, context=locals())

    def post(self, request, *args, **kwargs):
        id_aeroporto   = kwargs['id_aeroporto']
        aeroporto      = get_object_or_404(Aeroporto, pk=id_aeroporto)
        aeroporto_form = self.form_class(request.POST, instance=aeroporto)
        if aeroporto_form.is_valid():
            aeroporto_form.save() 
            messages.success(request, '<strong> Aeroporto salvo com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:aeroportos'))
