from passagem.model.passagem import Passagem
from util.group_required_mixin import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
from passagem.model.passageiro_passagem import PassageiroPassagem
from passagem.model.solicitacao_passagem import SolicitacaoPassagem
from passagem.model.passageiro import Passageiro
from passagem.model.companhia import Companhia
from passagem.forms.passageiro_passagem_form import PassageiroPassagemForm
from passagem.model.cota import Cota
from passagem.model.passagem import Passagem
from auth_local.util.email import enviar_email_passagens_emitida, enviar_email_passagem_remarcada
from passagem.model.remarcacao_passagem import RemarcacaoPassagem
from passagem.model.passagem import Passagem
from passagem.model.passageiro_passagem import PassageiroPassagem
from passagem.forms.remarcacao_passagem_form import RemarcacaoPassagemForm
from datetime import date
from datetime import datetime


class PassageiroPassagemCreateView(GroupRequiredMixin, CreateView):
    model = PassageiroPassagem
    form_class = PassageiroPassagemForm
    template_name = 'passagem/passageiro_passagem.html'
    
    @method_decorator(login_required)
    def get(self, request, id_passageiro, id_solicitacao_passagem, id_passagem):
        passageiro_passagem_form = self.form_class(use_required_attribute=False)
        #passagem = Passagem.objects.get(pk=id_passagem)
        passageiro_passagem = PassageiroPassagem.objects.get(passageiro=id_passageiro, passagem=id_passagem)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)

        return render(request, self.template_name, context=locals())
    
  
    def post(self, request, *args, **kwargs):
        passageiro_passagem_form = self.form_class(request.POST)
        passageiro_passagem = PassageiroPassagem.objects.get(passageiro=kwargs['id_passageiro'], passagem=kwargs['id_passagem'])
        passagem = Passagem.objects.get(pk=kwargs['id_passagem'])
        if passageiro_passagem_form.is_valid():
            passageiro_passagem.passagem = Passagem.objects.get(pk=kwargs['id_passagem'])
            passageiro_passagem.passageiro = Passageiro.objects.get(pk=kwargs['id_passageiro'])
            passageiro_passagem.num_bilhete = request.POST.get("num_bilhete")
            passageiro_passagem.num_voo = request.POST.get("num_voo")
            passageiro_passagem.companhia = Companhia.objects.get(pk=request.POST.get("companhia"))
            passageiro_passagem.tarifa = request.POST.get("tarifa")
            passageiro_passagem.valor_embarque = request.POST.get("valor_embarque")
            passageiro_passagem.valor = request.POST.get("valor")
            passageiro_passagem.taxa_servico = request.POST.get("taxa_servico")
            passageiro_passagem.status = "C"
            passageiro_passagem.data_viagem = datetime.strptime(request.POST.get("data_viagem"), '%d/%m/%Y %H:%M')
            passageiro_passagem.save()
            solicitacao_passagem = SolicitacaoPassagem.objects.filter(passagens__in=[passageiro_passagem.passagem])[0]
            usuario = solicitacao_passagem.usuario
            enviar_email_passagens_emitida(usuario, passageiro_passagem)
            messages.success(request, 'Passagem emitida para <strong> ' + passageiro_passagem.passageiro.nome + '</strong> foi salvo(a) com sucesso.')
            return redirect('passagem:acompanhamento_solicitacao_passagem', kwargs['id_solicitacao_passagem'])
        else:
            print(passageiro_passagem_form.errors)
        
        return render(request, self.template_name, context=locals())  
    


class PassageiroPassagemUpdateView(GroupRequiredMixin, UpdateView):
    model = PassageiroPassagem
    form_class = PassageiroPassagemForm
    template_name = 'passagem/passageiro_passagem.html'
    
    @method_decorator(login_required)
    def get(self, request, id_passageiro, id_passagem, id_solicitacao_passagem):
        passageiro_passagem = get_object_or_404(PassageiroPassagem, passageiro=id_passageiro, passagem=id_passagem)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        #acompanhamentos = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem)
        passageiro_passagem_form = self.form_class(instance=passageiro_passagem)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        passageiro_passagem = get_object_or_404(PassageiroPassagem, passageiro=kwargs['id_passageiro'], passagem=kwargs['id_passagem'])
        solicitacao_passagem = SolicitacaoPassagem.objects.filter(pk=kwargs['id_solicitacao_passagem'])
        
        #acompanhamentos = AcompanhamentoSolicitacaoPassagem.objects.filter(solicitacao_passagem=solicitacao_passagem)
        passageiro_passagem_form = self.form_class(request.POST, request.FILES, instance=passageiro_passagem)
        if passageiro_passagem_form.is_valid():
            passageiro_passagem_form.save()
            return HttpResponseRedirect(reverse('passagem:acompanhamento_solicitacao_passagem', args=(int(kwargs['id_solicitacao_passagem']),)))
        return render(request, self.template_name, context=locals())

class  TrechoDeleteView(GroupRequiredMixin, DeleteView):
    medel = Passagem   
    
    def get(self, request, id_passagem, id_solicitacao_passagem):
        passagem = get_object_or_404(Passagem, pk=id_passagem)
        solicitacao_passagem = get_object_or_404(SolicitacaoPassagem, pk=id_solicitacao_passagem)
        data_atual = datetime.now()
        if passagem:
            passagem.passageiros.remove()
            passagem.delete()
            cota = Cota.objects.get(orgao=solicitacao_passagem.orgao, exercicio=data_atual.year)
            cota.quantidade = cota.quantidade + 1
            cota.save()
            messages.success(request, 'O trecho foi deletado com sucesso. ')
            return HttpResponseRedirect(reverse('passagem:solicitacao_passagem_rota_add', args=(int(solicitacao_passagem.pk),)))


class RemarcacaoPassagemCreateView(GroupRequiredMixin, CreateView):
    model      = RemarcacaoPassagem
    form_class = RemarcacaoPassagemForm
    template_name   = 'passagem/remarcacao_passagem.html'

    def get(self, request, id_passageiro_passagem, id_solicitacao_passagem):
        passageiro_passagem_form = self.form_class(use_required_attribute=False)
        passageiro_passagem = PassageiroPassagem.objects.get(pk=id_passageiro_passagem)
        #passagem = Passagem.objects.get(pk=id_passagem)
        #remarcacao_passagem = RemarcacaoPassagem.objects.get(passagem=id_passagem)
        #passagem = Passagem.objects.get(pk=id_solicitacao_passagem)
        return render(request, self.template_name, context=locals())

    def post(self, request, *args, **kwargs):
        remarcacao_passagem_form = self.form_class(request.POST)
        passageiro_passagem = PassageiroPassagem.objects.get(pk=kwargs['id_passageiro_passagem'])
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=kwargs['id_solicitacao_passagem'])
        if remarcacao_passagem_form.is_valid():
            remarcacao_passagem = remarcacao_passagem_form.save(commit=False)
            remarcacao_passagem.data_remarcacao = date.today()
            remarcacao_passagem.passageiro_passagem = passageiro_passagem
            remarcacao_passagem.save()
            enviar_email_passagem_remarcada(solicitacao_passagem.usuario, remarcacao_passagem)
            messages.success(request, 'Passagem remarcada com sucesso para <strong> ' + passageiro_passagem.passageiro.nome + '</strong>.')
            return redirect('passagem:acompanhamento_solicitacao_passagem', kwargs['id_solicitacao_passagem'])
        return render(request, self.template_name, context=locals())




