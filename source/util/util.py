from datetime import datetime
import hashlib
import json
import random
from string import ascii_letters, digits
import urllib
import requests
from urllib.request import Request

from django.conf import settings
from django.http import HttpResponse
from django.template import Library
from django.utils import translation
from django.utils.formats import date_format
from auth_local.models.usuario_orgao import UsuarioOrgao

register = Library()


def anos_choice(interval=5):
    anos = []
    for r in range((datetime.datetime.now().year - interval),
                   (datetime.datetime.now().year + interval)):
        anos.append((r, r))
    return anos


def gerar_relatorio_ireport(id_usuario, id_manifestacao):
    params = {}
    relatorio = 'report_print_manifestacao'

    if id_manifestacao:
        params['INT_ID_MANIFESTACAO'] = int(id_manifestacao)
        params['INT_ID_USUARIO'] = int(id_usuario)
        params['relatorio'] = relatorio

        return download_relatorio(relatorio, params)

    return ""


def download_relatorio(relatorio, params):
    params['path_img'] = 'img'
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = Request(settings.IP_RELATORIO)

    with urllib.request.urlopen(req, data=data) as f:
        pdf = f.read()

    response_pdf = HttpResponse(pdf, content_type='application/pdf')
    response_pdf['Content-Disposition'] = 'filename=' + relatorio + '.pdf'

    return response_pdf


def get_name_month(data):
    if data:
        translation.activate('pt-BR')
        return date_format(data, 'F')
    return ""


def criar_hash():
    origem = ascii_letters + digits
    variavel = ''.join(random.choice(origem) for n in range(len(origem)))
    hash = hashlib.sha1()
    hash.update(variavel.encode("utf-8"))

    return hash.hexdigest()


def id_formatado(pk):
    return '%05d' % pk


def is_recaptcha_success(recaptcha_response):
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }

    req = requests.post(settings.GOOGLE_RECAPTCHA_SITE_VERIFY, data=values)
    result = req.json()

    return result['success']


def is_meu_perfil_gestor_form_changed(meu_perfil_form):
    return 'telefone' in meu_perfil_form.changed_data or \
           'nome' in meu_perfil_form.changed_data or \
           'senha_atual' in meu_perfil_form.changed_data or \
           'nova_senha' in meu_perfil_form.changed_data or \
           'confirmar_senha' in meu_perfil_form.changed_data


def is_endereco_form_changed(endereco_form):
    return 'endereco_cep' in endereco_form.changed_data or \
           'logradouro' in endereco_form.changed_data or \
           'numero' in endereco_form.changed_data or \
           'complemento' in endereco_form.changed_data or \
           'endereco_cidade' in endereco_form.changed_data or \
           'endereco_bairro' in endereco_form.changed_data


# def get_endereco_novo_cidadao(endereco_form):
#     endereco_novo = Endereco()
# 
#     endereco_novo.municipio = endereco_form.cleaned_data['endereco_cidade']
#     endereco_novo.bairro = endereco_form.cleaned_data['endereco_bairro']
#     endereco_novo.complemento = endereco_form.cleaned_data['complemento']
#     endereco_novo.numero = endereco_form.cleaned_data['numero']
#     endereco_novo.logradouro = endereco_form.cleaned_data['logradouro']
#     endereco_novo.cep = endereco_form.cleaned_data['endereco_cep']
# 
#     return endereco_novo


def get_gestor_by_id(id_gestor):
    try:
        return UsuarioOrgao.objects.get(pk=id_gestor)
    except UsuarioOrgao.DoesNotExist:
        return None


# def get_cidadao_by_id(id_cidadao):
#     try:
#         return UsuarioCidadao.objects.get(pk=id_cidadao)
#     except UsuarioCidadao.DoesNotExist:
#         return None

def get_context_sala_controle(context, manifestacoes):
    total_01_day = 0
    total_10_days = 0
    total_20_days = 0
    total_30_days = 0
    total_acima_30_days = 0
    total_andamento = 0

    for manifestacao in manifestacoes:
        total_dias = manifestacao.data_previsao_resposta - manifestacao.data_abertura
        progresso = datetime.today().date() - manifestacao.data_abertura
        dias_restantes = int((total_dias - progresso).days)

        if not manifestacao.is_encerrada():
            total_andamento += 1
        else:
            if dias_restantes <= 1:
                total_01_day += 1
            else:
                if dias_restantes <= 10:
                    total_10_days += 1
                elif dias_restantes > 10 and dias_restantes <= 20:
                    total_20_days += 1
                elif dias_restantes > 20 and dias_restantes <= 30:
                    total_30_days += 1
                else:
                    total_acima_30_days = + 1

    context['total_01_day'] = total_01_day
    context['total_10_days'] = total_10_days
    context['total_20_days'] = total_20_days
    context['total_30_days'] = total_30_days
    context['total_acima_30_days'] = total_acima_30_days
    context['total_andamento'] = total_andamento

    return context
