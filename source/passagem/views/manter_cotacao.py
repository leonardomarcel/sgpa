from passagem.model.cotacao import Cotacao
from passagem.model.passagem import Passagem
from passagem.model.solicitacao_passagem import SolicitacaoPassagem
from util.group_required_mixin import GroupRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from passagem.forms.cotacao_passagem_form import CotacaoPassagemForm
from django.contrib import messages


class CotacaoPassagemCreateView(GroupRequiredMixin, CreateView):
    model = Cotacao
    
    form_class = CotacaoPassagemForm
    template_name = 'solicitacao_passagem/cadastrar_cotacao.html'

    @method_decorator(login_required)
    def get(self, request, id_solicitacao_passagem, id_passagem):
        passagem = Passagem.objects.get(pk=id_passagem)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        cotacao_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())
    
    def post(self, request, *args, **kwargs):
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=kwargs['id_solicitacao_passagem'])
        passagem = Passagem.objects.get(pk=kwargs['id_passagem'])
        cotacoes = Cotacao.objects.filter(passagem=passagem)
        cotacoes.delete()
        cotacao_form = self.form_class(request.POST, use_required_attribute=False, initial={'orgao':self.request.user.orgao.id})
        if cotacao_form.is_valid():
            cotacao = cotacao_form.save(commit=False)
            passagem = Passagem.objects.get(pk=kwargs['id_passagem'])
            cotacao.passagem = passagem
            cotacao.save()
            
            #return redirect(reverse_lazy('passagem:solicitacao_passagem_rota_add ', kwargs={'pk': solicitacao_passagem.id}))
            return HttpResponseRedirect(reverse('passagem:acompanhamento_solicitacao_passagem', args=(int(solicitacao_passagem.id),)))
        
        return render(request, self.template_name, context=locals())

class CotacaoPassagemUpdateView(GroupRequiredMixin, UpdateView):
    model = Cotacao
    form_class = CotacaoPassagemForm
    template_name = 'solicitacao_passagem/cadastrar_cotacao.html'

    def get(self, request, id_cotacao, id_solicitacao_passagem):
        cotacao = get_object_or_404(Cotacao, pk=id_cotacao)
        solicitacao_passagem = SolicitacaoPassagem.objects.get(pk=id_solicitacao_passagem)
        cotacao_form = self.form_class(instance=cotacao)
        return render(request, self.template_name, context=locals())

    def post(self, request, *args, **kwargs):
        cotacao = get_object_or_404(Cotacao, pk=kwargs['id_cotacao'])
        solicitacao_passagem = get_object_or_404(SolicitacaoPassagem, pk=kwargs['id_solicitacao_passagem'])
        cotacao_form = self.form_class(request.POST, instance=cotacao)
        if cotacao_form.is_valid():
            cotacao.save()
            messages.success(request, '<strong> Cotação editado com sucesso!</strong>')
            return HttpResponseRedirect(reverse('passagem:acompanhamento_solicitacao_passagem', args=(int(solicitacao_passagem.id),)))
        return render(request, self.template_name, context=locals())
    