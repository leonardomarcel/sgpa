from util.group_required_mixin import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from passagem.model.cota import Cota
from passagem.forms.cota_form import CotaForm
from auth_local.models.usuario_orgao import UsuarioOrgao

class CotaCreateView(GroupRequiredMixin, CreateView):
    model         = Cota
    form_class    = CotaForm
    template_name = 'cota/editar_cota.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    @method_decorator(login_required)
    def get(self, request):
        cota_form = self.form_class(use_required_attribute=False)

        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        cota_form = self.form_class(request.POST)
        if cota_form.is_valid():
            cota = cota_form.save(commit=False)
            cota.usuario_criacao = request.user
            cota.save()
            messages.success(request, '<strong> Cota salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:cotas'))
        return render(request, self.template_name, context=locals())
        


class CotaListView(GroupRequiredMixin, ListView):
    model = Cota
    template_name = 'cota/cota_list.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cotas = self.get_queryset().distinct()
        context['cotas'] = cotas
        page = int(self.request.GET.get('cotas_page', 1))
        context['cota_paginator'] = Paginator(cotas, 10).page(page)
        return context

class CotaUpdateView(GroupRequiredMixin, UpdateView):
    model         = Cota
    form_class    = CotaForm
    template_name = 'cota/editar_cota.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    #@method_decorator(login_required)
    def get(self, request, id_cota):
        cota = get_object_or_404(Cota, pk=id_cota)
        cota_form = self.form_class(instance=cota)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        id_cota = kwargs['id_cota']
        cota = get_object_or_404(Cota, pk=id_cota)
        cota_form = self.form_class(request.POST, instance=cota)
        if cota_form.is_valid():
            cota_form.save() 
            messages.success(request, '<strong> Cota salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:cotas'))

