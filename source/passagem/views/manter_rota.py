from django.http import HttpResponseRedirect
from django.urls import reverse
from util.group_required_mixin import GroupRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from passagem.model.rota import Rota
from passagem.forms.rota_form import RotaForm
from auth_local.models.usuario_orgao import UsuarioOrgao

class RotaCreateView(GroupRequiredMixin, CreateView):
    model = Rota
    form_class = RotaForm
    template_name = 'rota/editar_rota.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get(self, request):
        rota_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        rota_form = self.form_class(request.POST)
        if rota_form.is_valid():
            rota_form.save()
            messages.success(request, '<strong> Rota salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:rotas'))
        return render(request, self.template_name, context=locals())

class RotaListView(GroupRequiredMixin, ListView):
    model = Rota
    template_name = 'rota/rota_list.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rotas = self.get_queryset().distinct()
        context['rotas'] = rotas
        page = int(self.request.GET.get('rotas_page', 1))
        context['rota_paginator'] = Paginator(rotas, 10).page(page)
        return context


class RotaUpdateView(GroupRequiredMixin, UpdateView):
    model = Rota
    form_class = RotaForm
    template_name = 'rota/editar_rota.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get(self, request, id_rota):
        rota       = get_object_or_404(Rota, pk=id_rota)
        rota_form  = self.form_class(instance=rota)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        id_rota   = kwargs['id_rota']
        rota      = get_object_or_404(Rota, pk=id_rota)
        rota_form = self.form_class(request.POST, instance=rota)
        if rota_form.is_valid():
            rota_form.save() 
            messages.success(request, '<strong> Rota salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:rotas'))








