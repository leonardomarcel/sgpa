# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#import ssl
import functools
from util.group_required_mixin import GroupRequiredMixin

from passagem.model.passageiro_passagem import PassageiroPassagem
from passagem.model.remarcacao_passagem import RemarcacaoPassagem
from basico.models.orgao import Orgao
from relatorio.forms import PassagemPeriodoForm
from passagem.model.passagem import Passagem

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from django_weasyprint.utils import django_url_fetcher
from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateResponse 
from django_weasyprint.views import CONTENT_TYPE_PNG

#########################################
import tempfile

def total_passagens(passagens, orgao=None):
    if orgao:
        orgaos = Orgao.objects.filter(pk=orgao.id)
    else:
        orgaos = Orgao.objects.all()
    lista_passagens_orgao = []
    for orgao in orgaos:
        orgao_passagens = {}
        orgao_passagens['orgao'] = orgao
        passagens = PassageiroPassagem.objects.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__orgao=orgao), status='C')
        total = 0
        qtd_passagem = passagens.count()
        for passagem in passagens:
            total = total + passagem.total()
        orgao_passagens['total'] = total
        orgao_passagens['quantidade'] = qtd_passagem
        lista_passagens_orgao.append(orgao_passagens)
    return lista_passagens_orgao


class RelatorioPassagemPeriodo(GroupRequiredMixin, TemplateView):
    medel = PassageiroPassagem()
    template_name = 'form_relatorio_passagens_periodo.html' 
    form_class = PassagemPeriodoForm

    @method_decorator(login_required)
    def get(self, request):
        passagem_periodo_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())
    def post(self, request):
        passagem_periodo_form = self.form_class(request.POST)
        if passagem_periodo_form.is_valid():
            data_inicio = passagem_periodo_form.cleaned_data['data_inicio']
            data_final = passagem_periodo_form.cleaned_data['data_termino']
            orgao = passagem_periodo_form.cleaned_data['orgao']
            agencia_viagem = passagem_periodo_form.cleaned_data['agencia_viagem']
            cia_aerea = passagem_periodo_form.cleaned_data['cia_aerea']
            motivo = passagem_periodo_form.cleaned_data['motivo']
            passageiro = passagem_periodo_form.cleaned_data['passageiro']
            urgente = passagem_periodo_form.cleaned_data['urgente']

            passagens = PassageiroPassagem.objects.filter(data_viagem__gte=data_inicio, data_viagem__lte=data_final, status='C')
            remarcacoes = RemarcacaoPassagem.objects.filter(passageiro_passagem__in=passagens)
            
            if orgao:
                orgao = Orgao.objects.get(pk=orgao.id)
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__orgao=orgao))
            if agencia_viagem:
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(agencia=agencia_viagem))
            if cia_aerea:
                passagens = passagens.filter(companhia=cia_aerea)
            if motivo:
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__motivo=motivo))
            if passageiro:
                passagens = passagens.filter(passageiro=passageiro)
            if urgente:
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__urgente=urgente))

            
            return render(request, 'relatorio_analitico_passagem_periodo.html', context=locals())

            # font_config = FontConfiguration()
            # settings.STATIC_ROOT + 'css/app.css'
            # estilo_relatorio = open(settings.RELATORIO_CSS)
            # css = CSS(string=estilo_relatorio.read())
            # # css = CSS(string='''
            # # .box-trecho {
            # # background-color:#F0F8FF;
            # # border: 1px solid;
            # # margin: 3px;
            # # font-size: 12px;
            # # padding: 8px;

            # # }''', font_config=font_config)

            # # Rendered
            # html_string = render_to_string('relatorio_analitico_passagem_periodo.html', {'passagens': passagens})
            # html = HTML(string=html_string)
            # result = html.write_pdf(stylesheets=[css], font_config=font_config)

            # # Creating http response
            # response = HttpResponse(content_type='application/pdf; charset=utf-8')
            # #response['Content-Disposition'] = 'inline; filename=list_people.pdf'
            # #response['Content-Transfer-Encoding'] = 'binary'
            # with tempfile.NamedTemporaryFile(delete=True) as output:
            #     output.write(result)
            #     output.flush()
            #     output = open(output.name, 'rb')
            #     response.write(output.read())

            # #return response



class RelatorioContabilPassagemPeriodo(GroupRequiredMixin, TemplateView):
    template_name = 'form_relatorio_passagens_periodo.html' 
    form_class = PassagemPeriodoForm

    @method_decorator(login_required)
    def get(self, request):
        passagem_periodo_form = self.form_class(use_required_attribute=False)
        return render(request, self.template_name, context=locals())

    def post(self, request):
        passagem_periodo_form = self.form_class(request.POST)
        if passagem_periodo_form.is_valid():
            data_inicio = passagem_periodo_form.cleaned_data['data_inicio']
            data_final = passagem_periodo_form.cleaned_data['data_termino']
            orgao = passagem_periodo_form.cleaned_data['orgao']
            agencia_viagem = passagem_periodo_form.cleaned_data['agencia_viagem']
            cia_aerea = passagem_periodo_form.cleaned_data['cia_aerea']
            motivo = passagem_periodo_form.cleaned_data['motivo']
            passageiro = passagem_periodo_form.cleaned_data['passageiro']
            urgente = passagem_periodo_form.cleaned_data['urgente']

            passagens = PassageiroPassagem.objects.filter(data_viagem__gte=data_inicio, data_viagem__lte=data_final, status='C')
            remarcacoes = RemarcacaoPassagem.objects.filter(passageiro_passagem__in=passagens)
            
            if orgao:
                orgao = Orgao.objects.get(pk=orgao.id)
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__orgao=orgao))
            if agencia_viagem:
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(agencia=agencia_viagem))
            if cia_aerea:
                passagens = passagens.filter(companhia=cia_aerea)
            if motivo:
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__motivo=motivo))
            if passageiro:
                passagens = passagens.filter(passageiro=passageiro)
            if urgente:
                passagens = passagens.filter(passagem__in=Passagem.objects.filter(solicitacaopassagem__urgente=urgente))
            if orgao:
                totais = total_passagens(passagens, orgao)
            else:
                totais = total_passagens(passagens)

                
            return render(request, 'relatorio_contabil_passagem_periodo.html', context=locals())



def generate_pdf(request, id_passageiro_passagem):
    """Generate pdf."""
    # Model data
    font_config = FontConfiguration()
    passageiro_passagem = get_object_or_404(PassageiroPassagem, pk=id_passageiro_passagem)
    remarcacoes = RemarcacaoPassagem.objects.filter(passageiro_passagem=passageiro_passagem)

    css = CSS(string='''
    .box-trecho {
	background-color:#F0F8FF;
	border: 1px solid;
	margin: 3px;
    font-size: 12px;
	padding: 8px;

}''', font_config=font_config)

    # Rendered
    html_string = render_to_string('passagem_emitida.html', {'passageiro_passagem': passageiro_passagem,
    'remarcacoes': remarcacoes})
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[css], font_config=font_config)

    # Creating http response
    response = HttpResponse(content_type='application/pdf; charset=utf-8')
    #response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    #response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response



class MyModelView(DetailView):
    # vanilla Django DetailView
    model = PassageiroPassagem
    template_name = 'passagem_emitida.html'

class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to change the default URL fetcher
    def get_url_fetcher(self, **kwargs):
        context = super().get_url_fetcher(**kwargs)
        # disable host and certificate check
        #context = ssl.create_default_context()
        #context.check_hostname = False
        #context.verify_mode = ssl.CERT_NONE
        passageiro_passagem = get_object_or_404(PassageiroPassagem, pk=73)
        remarcacoes = RemarcacaoPassagem.objects.filter(passageiro_passagem=passageiro_passagem)
        context.passageiro_passagem = passageiro_passagem
        context.remarcacoes = remarcacoes
        # print(context.passageiro_passagem.passageiro.cpf)
        return context
    
    def get_document(self, **kwargs):
        font_config = FontConfiguration()
        passageiro_passagem = get_object_or_404(PassageiroPassagem, pk=73)
        html_string = render_to_string('passagem_emitida.html', {'passageiro_passagem': passageiro_passagem})
        css = CSS(string='''
        .box-trecho {
        background-color:#F0F8FF;
        border: 1px solid;
        margin: 3px;
        padding: 8px;

    }''', font_config=font_config)

        
        html = HTML(string=html_string)
        htm_css = html.write_pdf(stylesheets=[css], font_config=font_config)
        return htm_css
    

class MyModelPrintView(WeasyTemplateResponseMixin, MyModelView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        'http://localhost:8000/static/css/passagem/solicitacao_passagem.css'
        #settings.STATIC_ROOT + 'css/app.css',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse

class MyModelDownloadView(WeasyTemplateResponseMixin, MyModelView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'

class MyModelImageView(WeasyTemplateResponseMixin, MyModelView):
    # generate a PNG image instead
    content_type = CONTENT_TYPE_PNG

    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )