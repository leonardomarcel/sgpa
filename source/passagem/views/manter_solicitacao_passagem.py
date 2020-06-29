from util.group_required_mixin import GroupRequiredMixin
from util.util import get_gestor_by_id 
from django.views.generic.list import ListView
from datetime import date
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from passagem.model.solicitacao_passagem import SolicitacaoPassagem
from passagem.model.cotacao import Cotacao
from passagem.forms.solicitacao_passagem_form import SolicitacaoPassagemForm,\
    SolicitacaoPassagemBuscarForm, AcompanhamentoSolicitacaoPassagemForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib import messages
from passagem.forms.solicitacao_passagem_rota_form import SolicitacaoPassagemRotaForm
from basico.models.orgao import Orgao
from django.http import HttpResponseRedirect
from passagem.model.passagem import Passagem
from passagem.model.rota import Rota
from passagem.model.trecho import Trecho
from passagem.model.passageiro import Passageiro
from passagem.model.passageiro_passagem import PassageiroPassagem
from passagem.forms.solicitacao_passagem_passageiro_form import SolicitacaoPassagemPassageiroForm
from passagem.model.cota import Cota
from passagem.model.anexo_processo_solicitacao_passagem import AnexoProcessoSolicitacaoPassagem
from passagem.model.remarcacao_passagem import RemarcacaoPassagem
from django.core.paginator import Paginator
from passagem.model.acompanhamento_solicitacao_passagem import AcompanhamentoSolicitacaoPassagem
from auth_local.models.usuario_orgao import UsuarioOrgao
from auth_local.util.email import enviar_email_solicitacao_passagem_criada, enviar_email_solicitacao_passagem_aprovada,\
    enviar_email_solicitacao_passagem_reprovada
from datetime import datetime
from django.db.models import Prefetch
import os
from django.conf import settings
from django.utils.safestring import mark_safe
from datetime import timedelta
from math import radians, cos, sin, asin, sqrt



def calcular_distancia(a, b):
    # Raio da Terra em Km
    r = 6371

    # Converte coordenadas de graus para radianos
    lon1, lat1, lon2, lat2 = map(radians, [ a.longitude, a.latitude, b.longitude, b.latitude ] )

    # Formula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    hav = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    d = 2 * r * asin( sqrt(hav) )

    return d


def solicitacao_passagem_no_prazo(data_ida):
    lista_dias = (0,1,2,3,4)
    contador = 0
    if data_ida:
        dias = (data_ida - date.today()).days   
        for i in range(dias):
            data_solic = date.today()
            prox_dia = data_solic + timedelta(days=i)
            
            if prox_dia.weekday() in lista_dias:                    
                contador+=1                   
                #data_solic = data_solic+timedelta(days=1)                                
        if contador<5: 
            return False
        else:
            return True
            #messages.error(request, 'solicitação de passagem fora do prazo mínimo de 05 dias úteis.  '+ mark_safe('<a href="" data-toggle="modal" data-target="#modalLoginForm" >Clique para justificar</a>')

def subtrai_cota(orgao, quantidade):
    cota = None
    try:
        cota = Cota.objects.get(orgao=orgao, exercicio=date.today().year)
    except:
        pass
    cota.quantidade = cota.quantidade - quantidade 
    cota.save()

def verifica_quantidade_cota(orgao):
    cota = None
    quantidade = 0
    try:
        cota = Cota.objects.get(orgao=orgao.id, exercicio=date.today().year)
    except:
        pass
    if cota:
        quantidade = cota.quantidade
    return quantidade

class SolicitacaoPassagemListView(GroupRequiredMixin, ListView):
    model      = SolicitacaoPassagem
    form_class = SolicitacaoPassagemBuscarForm
    template_name   = "solicitacao_passagem/solicitacaopassagem_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitacoes_passagem = self.get_queryset().distinct()
        prefetch_passagem = Prefetch("passagens__passageiropassagem_set",
        queryset=PassageiroPassagem.objects.filter(status='C'),
        to_attr="tem_passageiro_passagem")
        solicitacoes_passagem = solicitacoes_passagem.prefetch_related(prefetch_passagem)
        
        context['buscar_form'] = self.form_class(self.request.GET)
        context['solicitacoes_passagem'] = solicitacoes_passagem
        page = int(self.request.GET.get('solicitacoes_passagem_page', 1))
        context['solicitacoes_passagem_paginator'] = Paginator(solicitacoes_passagem, 5).page(page)
        return context
        
    def get_queryset(self):
        usuario = UsuarioOrgao.objects.get(pk=self.request.user.id)
        request = self.request.GET
        buscar_form = self.form_class(self.request.GET)
        gestor = get_gestor_by_id(self.request.user.id)
        if usuario.is_agencia_viagem() or usuario.is_superuser:
            solocitacoes_passagem = super(SolicitacaoPassagemListView, self).get_queryset().filter(status='AUTORIZADA').order_by('data')
        else:
            solocitacoes_passagem = super(SolicitacaoPassagemListView, self).get_queryset().all().order_by('data')
        
        if buscar_form.is_valid():
            inicio = request.get('inicio')
            termino = request.get('termino')
            status = request.get('status')
            codigo = request.get('codigo')

            if inicio and termino:
                inicio = datetime.strptime(inicio, '%d/%m/%Y')
                termino = datetime.strptime(termino, '%d/%m/%Y')
                solocitacoes_passagem = solocitacoes_passagem.filter(data__gte=inicio, data__lte=termino)
            if status:
                if status =="TODAS":
                    solocitacoes_passagem = solocitacoes_passagem.all()
                else:
                    solocitacoes_passagem = solocitacoes_passagem.filter(status=status)
            if codigo:
                try:
                     solocitacoes_passagem = solocitacoes_passagem.filter(codigo=int(codigo))
                except:
                    pass
            
       
        return solocitacoes_passagem
        
class SolicitacaoPassagemCreateView(GroupRequiredMixin, CreateView):
    model = SolicitacaoPassagem
    
    form_class = SolicitacaoPassagemForm
    template_name = 'solicitacao_passagem/solicitacao_passagem.html'

    @method_decorator(login_required)
    def get(self, request):
        #if request.session.get('step', "") not in ("solicitacao_passagem_criacao"): 
            #return redirect("tipo_ocorrencia", id_boletim=id_boletim)
        solicitacao_passagem_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        request.session['step'] = "solicitacao_passagem_criacao"
        solicitacao_passagem_form = self.form_class(request.POST,  request.FILES, use_required_attribute=False, initial={'orgao':self.request.user.orgao.id})
        cota_quantidade = verifica_quantidade_cota(self.request.user.orgao)
        if solicitacao_passagem_form.is_valid():
            if cota_quantidade > 0 :
                solicitacao_passagem = solicitacao_passagem_form.save(commit=False)
                solicitacao_passagem.orgao = self.request.user.orgao
                solicitacao_passagem.usuario = self.request.user
                solicitacao_passagem.status = 'ABERTA'
                solicitacao_passagem.data = date.today()
                solicitacao_passagem.usuario = self.request.user
                solicitacao_passagem.codigo
                solicitacao_passagem.save()
                solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=solicitacao_passagem.pk)
                solicitacao_passagem.codigo = solicitacao_passagem.pk
                anexos_processo = self.request.FILES.getlist('anexos_processo')
                if anexos_processo:
                    count = 0
                    for arquivo in anexos_processo:
                        count += 1
                        anexo_processo_solicitacao_passagem = AnexoProcessoSolicitacaoPassagem()
                        anexo_processo_solicitacao_passagem.nome = 'anexo_'+str(count) 
                        anexo_processo_solicitacao_passagem.tamanho = str(arquivo.size)
                        anexo_processo_solicitacao_passagem.arquivo = arquivo
                        anexo_processo_solicitacao_passagem.data_cadastro = date.today
                        anexo_processo_solicitacao_passagem.save()
                        solicitacao_passagem.anexos_processo.add(anexo_processo_solicitacao_passagem)

                solicitacao_passagem.save()
            else:
                messages.error(request, "Você não tem mais cota para solicitar passagem! Entre em contato com a Gestão de Passagens Aéreas da AMGESP")
                return redirect('passagem:solicitacao_passagem_add')
            
            #return redirect(reverse_lazy('passagem:solicitacao_passagem_rota_add ', kwargs={'pk': solicitacao_passagem.id}))
            return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_rota_add', args=(int(solicitacao_passagem.pk),)))
        else:
            print(solicitacao_passagem_form.errors)
        return render(request, self.template_name, context=locals())
    
class SolicitacaoPassagemUpdateView(GroupRequiredMixin, UpdateView):
    model = SolicitacaoPassagem
    form_class = SolicitacaoPassagemForm
    template_name = 'solicitacao_passagem/solicitacao_passagem.html'
    
    @method_decorator(login_required)
    def get(self, request, id_solicitacao_passagem):
        solicitacao_passagem = get_object_or_404(SolicitacaoPassagem, pk=id_solicitacao_passagem)
        acompanhamentos  = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem)
        anexos_processos = AnexoProcessoSolicitacaoPassagem.objects.filter(pk__in=solicitacao_passagem.anexos_processo.all()) 
        solicitacao_passagem_form = self.form_class(instance=solicitacao_passagem)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        request.session['step'] = "solicitacao_passagem_criacao"
        id_solicitacao_passagem = kwargs['id_solicitacao_passagem']
        solicitacao_passagem = get_object_or_404(SolicitacaoPassagem, pk=id_solicitacao_passagem)
        acompanhamentos = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem)
        solicitacao_passagem_form = self.form_class(request.POST, request.FILES, instance=solicitacao_passagem)
        if solicitacao_passagem_form.is_valid():
            solicitacao_passagem = solicitacao_passagem_form.save(commit=False)
            anexos_processo = self.request.FILES.getlist('anexos_processo')
            if anexos_processo:
                anexos_processo_solicitacao_passagem = AnexoProcessoSolicitacaoPassagem.objects.filter(pk__in=solicitacao_passagem.anexos_processo.all())
                for anexo in anexos_processo_solicitacao_passagem:
                    arquivo = os.path.join(settings.MEDIA_ROOT, str(anexo.arquivo))
                    os.remove(arquivo)
                    anexo.delete()

                count = 0
                for arquivo in anexos_processo:
                    count += 1
                    anexo_processo_solicitacao_passagem = AnexoProcessoSolicitacaoPassagem()
                    anexo_processo_solicitacao_passagem.nome = 'anexo_'+str(count) 
                    anexo_processo_solicitacao_passagem.tamanho = str(arquivo.size)
                    anexo_processo_solicitacao_passagem.arquivo = arquivo
                    anexo_processo_solicitacao_passagem.data_cadastro = date.today
                    anexo_processo_solicitacao_passagem.save()
                    solicitacao_passagem.anexos_processo.add(anexo_processo_solicitacao_passagem)
            solicitacao_passagem.save()
            return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_rota_add', args=(int(solicitacao_passagem.pk),)))
        return render(request, self.template_name, context=locals())
    
class SolicitacaoPassagemRotaCreateView(GroupRequiredMixin, TemplateView):
    medel = Passagem()
    template_name = 'solicitacao_passagem/solicitacao_passagem_rota.html' 
    form_class = SolicitacaoPassagemRotaForm
    
    def get(self, request, id_solicitacao_passagem):
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        if request.session.get('step', "") not in ("solicitacao_passagem_criacao", "solicitacao_passagem_rota_criacao"): 
            return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_conclusao_detail', args=(int(solicitacao_passagem.pk),)))
        acompanhamentos = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem)
        solicitacao_passagem_rota_form = self.form_class(orgao=request.user.orgao)
        passagens = Passagem.objects.filter(pk__in=solicitacao_passagem.passagens.all())
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        id_solicitacao_passagem = kwargs['id_solicitacao_passagem']
        usuario = UsuarioOrgao.objects.get(pk=self.request.user.id)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        acompanhamentos = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem)
        passagens            = Passagem.objects.filter(pk__in=solicitacao_passagem.passagens.all())
        solicitacao_passagem_rota_form = self.form_class(request.POST, orgao=request.user.orgao)

        justificativa = request.POST.get('justificativa')
        urgente = request.POST.get('urgente')
        if ('btn_cadastrar' in request.POST) or ('btn_cadastrar_justificativa' in request.POST):
            if solicitacao_passagem_rota_form.is_valid():
                tipo = solicitacao_passagem_rota_form.cleaned_data['tipo']
                origem   = solicitacao_passagem_rota_form.cleaned_data['origem']
                destino  = solicitacao_passagem_rota_form.cleaned_data['destino']
                data_ida =solicitacao_passagem_rota_form.cleaned_data['data_ida']
                data_volta =solicitacao_passagem_rota_form.cleaned_data['data_volta']
                passageiros = solicitacao_passagem_rota_form.cleaned_data['passageiros']
                cota = Cota.objects.get(orgao=self.request.user.orgao, exercicio=date.today().year)
                cota_quantidade = verifica_quantidade_cota(self.request.user.orgao)
                distancia = calcular_distancia(origem, destino)
                if distancia > 300:
                    if tipo == 'I':
                        solicitacao_no_prazo = solicitacao_passagem_no_prazo(data_ida)
                        if solicitacao_no_prazo == True or justificativa:
                            passagem = Passagem()
                            passagem.tipo = 'I'
                            rota = Rota.objects.get(origem=origem, destino=destino) 
                            passagem.rota = rota
                            passagem.data_viagem = data_ida
                            passagem.solicitacao = solicitacao_passagem
                            if urgente and justificativa:
                                passagem.justificativa_urgencia = justificativa
                                passagem.urgente = urgente
                                solicitacao_passagem.justificativa_urgencia = justificativa
                                solicitacao_passagem.urgente = urgente
                                solicitacao_passagem.save()
                            passagem.save()
                            for p in passageiros:
                                passagem.passageiros.add(p.id)
                            solicitacao_passagem.passagens.add(passagem)
                            subtrai_cota(self.request.user.orgao, len(passageiros))
                            solicitacao_passagem_rota_form = self.form_class(orgao=request.user.orgao)
                        else:
                            solicitacao_passagem_rota_form = self.form_class(request.POST, orgao=request.user.orgao)
                            messages.error(request, 'solicitação de passagem fora do prazo mínimo de 05 dias úteis.  '+ mark_safe('<a href="" data-toggle="modal" data-target="#modalLoginForm" >Clique para justificar</a>'))
                    else:
                        solicitacao_no_prazo = solicitacao_passagem_no_prazo(data_ida)
                        if solicitacao_no_prazo == True or justificativa:
                            ##Passagem de ida
                            passagem1 = Passagem()
                            passagem1.tipo = 'I'
                            rota = Rota.objects.get(origem=origem, destino=destino) 
                            passagem1.rota = rota
                            passagem1.data_viagem = data_ida
                            if urgente and justificativa:
                                passagem1.justificativa_urgencia = justificativa
                                passagem1.urgente = urgente
                                solicitacao_passagem.justificativa_urgencia = justificativa
                                solicitacao_passagem.urgente = urgente
                                solicitacao_passagem.save()
                            passagem1.save()
                            for p in passageiros:
                                passagem1.passageiros.add(p.id)
                            
                            ##passagem de volta
                            passagem2 = Passagem()
                            passagem2.tipo = 'V'
                            rota = Rota.objects.get(origem=destino, destino=origem) 
                            passagem2.rota = rota
                            passagem2.data_viagem = data_volta
                            if urgente and justificativa:
                                passagem2.justificativa_urgencia = justificativa
                                passagem2.urgente = urgente
                            passagem2.save()
                            for p in passageiros:
                                passagem2.passageiros.add(p.id)
                            
                            solicitacao_passagem.passagens.add(passagem1, passagem2)
                            solicitacao_passagem.justificativa_urgencia = justificativa
                            solicitacao_passagem.urgente  = urgente
                            solicitacao_passagem.save()
                            subtrai_cota(self.request.user.orgao, len(passageiros) *2)
                            solicitacao_passagem_rota_form = self.form_class(orgao=request.user.orgao)
                        else:
                            solicitacao_passagem_rota_form = self.form_class(request.POST, orgao=request.user.orgao)
                            messages.error(request, 'solicitação de passagem fora do prazo mínimo de 05 dias úteis.  '+ mark_safe('<a href="" data-toggle="modal" data-target="#modalLoginForm" >Clique para justificar</a>'))
                else:
                    solicitacao_passagem_rota_form = self.form_class(request.POST, orgao=request.user.orgao)
                    messages.error(request, 'Você não pode solicitar passagem com uma rota inferior a 300km.')
            
                return render(request, self.template_name, context=locals())
                #return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_rota_add', args=(int(solicitacao_passagem.pk),)))
        
        elif 'btn_concluir' in request.POST and passagens:
            if solicitacao_passagem.cadastro_concluido == False:
                solicitacao_passagem.cadastro_concluido = True
                solicitacao_passagem.save()
                enviar_email_solicitacao_passagem_criada(usuario, solicitacao_passagem, passagens)
            else:
                enviar_email_solicitacao_passagem_editada(usuario, solicitacao_passagem, passagens)
            return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_conclusao_detail', args=(int(solicitacao_passagem.pk),)))
        else:
            messages.error(request, "Você precisa cadastrar pelo menos 1 trecho para concluir a solicitação")
        return render(request, self.template_name, context=locals())
    
    
        
class SolicitacaoPassagemPassageiroCreateView(GroupRequiredMixin, CreateView):
    model = Passageiro
    form_class = SolicitacaoPassagemPassageiroForm
    template_name = 'solicitacao_passagem/solicitacao_passagem_passageiro.html'
    
    @method_decorator(login_required)
    def get(self, request, id_solicitacao_passagem):
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        solicitacao_passagem_passageiro_form = self.form_class()
        trechos = Trecho.objects.filter(solicitacao_passagem=solicitacao_passagem)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        solicitacao_passagem_passageiro_form = self.form_class(request.POST,  request.FILES, use_required_attribute=False)
        if solicitacao_passagem_passageiro_form.is_valid():
            solicitacao_passagem = solicitacao_passagem_passageiro_form.save(commit=False)
            orgao = Orgao.objects.get(pk=1)
            solicitacao_passagem.orgao = orgao
            solicitacao_passagem.save()
            
            #return redirect(reverse_lazy('passagem:solicitacao_passagem_rota_add ', kwargs={'pk': solicitacao_passagem.id}))
            return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_rota_add', args=(int(solicitacao_passagem.pk),)))
        return render(request, self.template_name, context=locals())
    
    

class AcompanhamentoSolicitacaoPassagemCreateView(GroupRequiredMixin, CreateView):
    model = AcompanhamentoSolicitacaoPassagem
    form_class = AcompanhamentoSolicitacaoPassagemForm
    template_name = 'solicitacao_passagem/acompanhamento_solicitacao_passagem.html'
    
    def get(self, request, id_solicitacao_passagem):
        acompanhamento_solicitacao_passagem_form = self.form_class(use_required_attribute=False)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        acompanhamentos      = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem).order_by('-data')
        passagens            = Passagem.objects.filter(pk__in=solicitacao_passagem.passagens.all())
        #cotacoes             = Cotacao.objects.filter(passagem__in=solicitacao_passagem.passagens.all())
    
        trechos              = Trecho.objects.filter(solicitacao_passagem=solicitacao_passagem)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        usuario = UsuarioOrgao.objects.get(pk=self.request.user.id)
        acompanhamento_solicitacao_passagem_form = self.form_class(request.POST, use_required_attribute=False)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=kwargs['id_solicitacao_passagem'])
        passagens            = Passagem.objects.filter(pk__in=solicitacao_passagem.passagens.all())
        acompanhamentos      = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem).order_by('-data')
        if acompanhamento_solicitacao_passagem_form.is_valid():
            acompanhamento_solicitacao_passagem = acompanhamento_solicitacao_passagem_form.save(commit=False)
            acompanhamento_solicitacao_passagem.usuario = request.user
            acompanhamento_solicitacao_passagem.data =date.today()
            acompanhamento_solicitacao_passagem.solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=kwargs['id_solicitacao_passagem'])
            status   = acompanhamento_solicitacao_passagem_form.cleaned_data['status']
            solicitacao_passagem.status = status
            solicitacao_passagem.save()
            acompanhamento_solicitacao_passagem.save()
            if status == "AUTORIZADA":
                enviar_email_solicitacao_passagem_aprovada(solicitacao_passagem.usuario, solicitacao_passagem, passagens)
            else:
                enviar_email_solicitacao_passagem_reprovada(solicitacao_passagem.usuario, acompanhamento_solicitacao_passagem)

            #return redirect(reverse_lazy('passagem:solicitacao_passagem_rota_add ', kwargs={'pk': solicitacao_passagem.id}))
            return HttpResponseRedirect(reverse('passagem:acompanhamento_solicitacao_passagem', args=(int(kwargs['id_solicitacao_passagem']),)))
        
        return render(request, self.template_name, context=locals())
    

class SolicitacaoPassagemConclucaoDetailView(GroupRequiredMixin, DetailView):
    model = SolicitacaoPassagem
    template_name = 'solicitacao_passagem/solicitacao_passagem_conclusao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['step'] = ""
        context['solicitacao_passagem'] = get_object_or_404(SolicitacaoPassagem, pk=self.kwargs['pk'])
        return context

class SolicitacaoPassagemPassagensDetailView(GroupRequiredMixin, DetailView):
    model = SolicitacaoPassagem
    template_name = 'solicitacao_passagem/solicitacao_passagem_passagens.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitacao_passagem = get_object_or_404(SolicitacaoPassagem, pk=self.kwargs['pk'])
        context['passageiros_passagens'] = PassageiroPassagem.objects.filter(passagem__in=solicitacao_passagem.passagens.all(), status='C')
        context['remarcacoes'] = RemarcacaoPassagem.objects.filter(passageiro_passagem__in=context['passageiros_passagens']).order_by('-data_viagem')
        context['solicitacao_passagem'] = solicitacao_passagem
        return context

