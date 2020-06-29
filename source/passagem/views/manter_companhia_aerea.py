
from util.group_required_mixin import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from passagem.model.companhia import Companhia
from passagem.forms.companhia_aerea_form import CompanhiaAereaForm
from auth_local.models.usuario_orgao import UsuarioOrgao

class CompanhiaAereaCreateView(GroupRequiredMixin, CreateView):
    model          = Companhia
    form_class     = CompanhiaAereaForm  
    template_name  = 'companhia/editar_companhia_aerea.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get(self, request):
        companhia_aerea_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())

    def post(self, request, *args, **kwargs):
        companhia_aerea_form = self.form_class(request.POST)
        if companhia_aerea_form.is_valid():
            companhia_aerea_form.save()
            messages.success(request, '<strong> Companhia  Aérea salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:aeroportos'))
        
        
        return render(request, self.template_name, context=locals())

class CompanhiaAereaListView(GroupRequiredMixin, ListView):
    model = Companhia
    template_name = 'companhia/companhia_aerea_list.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companhias_aereas = self.get_queryset().distinct()
        context['companhias_aereas'] = companhias_aereas
        page = int(self.request.GET.get('cotas_page', 1))
        context['companhia_aerea_paginator'] = Paginator(companhias_aereas, 10).page(page)
        return context

class CompanhiaAereaUpdateView(GroupRequiredMixin, UpdateView):
    model          = Companhia
    form_class     = CompanhiaAereaForm  
    template_name  = 'companhia/editar_companhia_aerea.html'
    group_required = [UsuarioOrgao.GROUP_GESTOR_AMGESP]

    #@method_decorator(login_required)
    def get(self, request, id_companhia_aerea):
        companhia_aerea = get_object_or_404(Companhia, pk=id_companhia_aerea)
        companhia_aerea_form = self.form_class(instance=companhia_aerea)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        id_companhia_aerea = kwargs['id_companhia_aerea']
        companhia_aerea = get_object_or_404(Companhia, pk=id_companhia_aerea)
        companhia_aerea_form = self.form_class(request.POST, instance=companhia_aerea)
        if companhia_aerea_form.is_valid():
            companhia_aerea_form.save() 
            messages.success(request, '<strong> Companhia Aérea salva com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:companhias_aereas'))




