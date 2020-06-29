from datetime import datetime

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render

from auth_local.models.usuario_orgao import UsuarioOrgao
from basico.models.orgao import Orgao
import manifestacao
from manifestacao.models.assunto import Assunto
from manifestacao.models.manifestacao import Manifestacao
from manifestacao.models.movimentacao import Movimentacao
from manifestacao.models.status import Status
from manifestacao.util.manifestacao_util import gerar_movimentacao_analise, \
    gerar_movimentacao_reabrir_manifestacao, get_data_previsao_resposta, \
    gerar_movimentacao_prorrogar_manifestacao, \
    get_data_prorrogacao_prazo, \
    get_proximo_dia_util, \
    get_data_previsao_complementacao, \
    gerar_movimentacao_arquivar_manifestacao, \
    gerar_movimentacao_informacao_pessoal, gerar_movimentacao_inserir_resposta, \
    gerar_movimentacao_ouvidoria_destino, get_tipo_manifestacao_choice_by_chave, \
    gerar_movimentacao_tipo_manifestacao, gerar_movimentacao_assunto,\
    gerar_movimentacao_remover_anexo, gerar_movimentacao_alterar_responsavel,\
    gerar_movimentacao_complementacao, gerar_movimentacao_ouvidoria_origem,\
    get_tipo_manifestacao_nome
from painel.forms.manifestacao_detalhes_form import ManifestacaoDetalhesForm
from manifestacao.models.manifestacao_anexo import ManifestacaoAnexo
import logging
from manifestacao.models.manifestacao_complementacao import ManifestacaoComplementacao
from auth_local.util import email
from util.util import get_gestor_by_id

def load_manifestacao(request, id_manifestacao):
    template_name = "manifestacao/detalhes/dados/manifestacao_body.html"
    try:
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)

        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[LOAD_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar assinalar a informação pessoal da manifestacao', status=401)
        
    return render(request, template_name, context=locals())

def reabrir_manifestacao(request):
    template_name = "manifestacao/detalhes/dados/manifestacao_body.html"
    id_manifestacao = request.POST.get('id_manifestacao')
    justificativa = request.POST.get('justificativa')
    
    try:
        if id_manifestacao:
            
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        
        movimentacao = gerar_movimentacao_reabrir_manifestacao(gestor, manifestacao, justificativa)
        movimentacao.save()
        
        status_analise = get_object_or_404(Status, pk = Status.ID_EM_ANALISE)
        
        texto_movimentacao = 'O status da manifestação foi alterado de '+ manifestacao.status.nome + ' para ' + status_analise.nome
        
        manifestacao.status = status_analise
        manifestacao.save()
        manifestacao.movimentacoes.add(movimentacao)
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Reaberta', texto_movimentacao)
            
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[REABRIR_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar assinalar a informação pessoal da manifestacao', status=401)
        
    return render(request, template_name, context=locals())
    
def remover_anexo(request):
    template_name = "manifestacao/detalhes/dados/anexo/table_anexos.html"
    try:
        id_manifestacao = request.POST.get('id_manifestacao')
        id_arquivo = request.POST.get('id_arquivo')
        
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
            anexo = get_object_or_404(ManifestacaoAnexo, pk = id_arquivo)
            nome_anexo = anexo.nome
            gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
            manifestacao.anexos.remove(anexo)
            movimentacao = gerar_movimentacao_remover_anexo(gestor, nome_anexo, manifestacao)
            movimentacao.save()
            manifestacao.movimentacoes.add(movimentacao)
            
    except Exception as e:
        logging.error('[REMOVER_ANEXO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar remover o anexo da manifestação', status=401)
                    
    return render(request, template_name, context=locals())

def prorrogar_prazo_manifestacao(request):
    template_name = "manifestacao/detalhes/dados/manifestacao_body.html"
    try:
        id_manifestacao = request.POST.get('id_manifestacao')
        justificativa = request.POST.get('justificativa')
        
        if id_manifestacao:
                manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        gestor = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        has_exists_prorrogado = manifestacao.movimentacoes.filter(tipo_alteracao=Movimentacao.CHAVE_PRORROGAR_PRAZO).exists()
        
        if has_exists_prorrogado:
            logging.error('[PRORROGAR_PRAZO_MANIFESTACAO] - Essa manifestação já possui um prazo prorrogado')
            return HttpResponse('Essa manifestação já foi prorrogada uma vez', status=401)
        
        proximo_dia_util = get_proximo_dia_util(manifestacao.data_previsao_resposta)
        data_previsao_resposta_prorrogada = get_data_prorrogacao_prazo(proximo_dia_util)
        movimentacao = gerar_movimentacao_prorrogar_manifestacao(gestor, manifestacao, justificativa, manifestacao.data_previsao_resposta, data_previsao_resposta_prorrogada)
        movimentacao.save()
        
        status_prorrogada = get_object_or_404(Status, pk = Status.ID_PRORROGADA)
        texto_movimentacao = 'O status da manifestação foi alterado de '+ manifestacao.status.nome + ' para ' + status_prorrogada.nome
        
        manifestacao.status = status_prorrogada
        manifestacao.data_previsao_resposta = data_previsao_resposta_prorrogada
        
        manifestacao.save()
        
        manifestacao.movimentacoes.add(movimentacao)
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Prorrogação de Prazo', texto_movimentacao)
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[PRORROGAR_PRAZO_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar assinalar a informação pessoal da manifestacao ', status=401)
        
    return render(request, template_name, context=locals())

def arquivar_manifestacao(request):
    template_name = "manifestacao/detalhes/dados/manifestacao_body.html"
    try:
        id_manifestacao = request.POST.get('id_manifestacao')
        justificativa = request.POST.get('justificativa')
        
        if id_manifestacao:
                manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        gestor = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        
        movimentacao = gerar_movimentacao_arquivar_manifestacao(gestor, manifestacao, justificativa)
        movimentacao.save()
        
        status_arquivada = get_object_or_404(Status, pk = Status.ID_ARQUIVADA)
        
        texto_movimentacao = 'O status da manifestação foi alterado de '+ manifestacao.status.nome + ' para ' + status_arquivada.nome
        
        manifestacao.status = status_arquivada
        manifestacao.save()
        manifestacao.movimentacoes.add(movimentacao)
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Reaberta', texto_movimentacao)
        
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[ARQUIVAR_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar assinalar a informação pessoal da manifestacao ', status=401)
        
    return render(request, template_name, context=locals())

def assinalar_informacao_pessoal(request, id_manifestacao, flag_informacao_pessoal):
    template_name = "manifestacao/detalhes/dados/manifestacao_body.html"

    try:
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        gestor = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        
        has_informacao_pessoal = flag_informacao_pessoal == 'S'
        movimentacao = gerar_movimentacao_informacao_pessoal(gestor, manifestacao, has_informacao_pessoal)
        movimentacao.save()
        
        manifestacao.has_informacao_pessoal = has_informacao_pessoal
        manifestacao.save()
        manifestacao.movimentacoes.add(movimentacao)
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
    except Exception as e:
        logging.error('[ASSINALAR_INFORMACAO_PESSOAL] - ' + str(e))
        return HttpResponse('Ocorreu um erro', status=401)
        
    return render(request, template_name, context=locals())

def analisar_manifestacao(request, id_manifestacao):
    template_name = "manifestacao/detalhes/analise/manifestacao_analise.html"

    try:
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        gestor = get_object_or_404(UsuarioOrgao, pk=request.user.id)
        
        if UsuarioOrgao.objects.filter(pk=request.user.id).exists():
            gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        
        status = get_object_or_404(Status, pk = Status.ID_EM_ANALISE)
        movimentacao = gerar_movimentacao_analise(gestor, manifestacao, status.nome)
        movimentacao.save()
        
        texto_movimentacao = 'O status da manifestação foi alterado de '+ manifestacao.status.nome + ' para ' + status.nome
        
        manifestacao.responsavel = gestor
        manifestacao.status = status
        
        manifestacao.data_inicio_analise = datetime.now()
        manifestacao.save()
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Em Análise', texto_movimentacao)
        
        manifestacao.movimentacoes.add(movimentacao)
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[ANALISAR_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um erro ao tentar analisar a manifestação', status=401)

    return render(request, template_name, context=locals())

def enviar_complementacao(request):
    template_name = "manifestacao/detalhes/dados/complementacao/complementacao_body.html"

    try:
        texto_complementacao = request.POST.get('complementacao')
        id_manifestacao = request.POST.get('id_manifestacao')
        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
 
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
             
        status = get_object_or_404(Status, pk = Status.ID_COMPLEMENTADA)
        
        texto_movimentacao = 'Foi solicitado um pedido de complementação, é necessário que você responda para prosseguir com o andamento da manifestação.'
        
        movimentacao = gerar_movimentacao_complementacao(gestor, manifestacao, texto_complementacao)
        movimentacao.save()
        
        complementacao = ManifestacaoComplementacao()
        complementacao.solicitacao = texto_complementacao
        complementacao.gestor = gestor
        today = datetime.now()
        proximo_dia_util = get_proximo_dia_util(today)
        data_limite = get_data_previsao_complementacao(proximo_dia_util)
        complementacao.data_limite_resposta = data_limite
        complementacao.save()
        
        manifestacao.status = status
        manifestacao.complementacao = complementacao
        
        manifestacao.save()
        manifestacao.movimentacoes.add(movimentacao)
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Pedido de Complementação', texto_movimentacao)
        
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[ENVIAR_COMPLEMENTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar enviar pedido de complementação para o cidadão', status=401)
   
    return render(request, template_name, context=locals())

def inserir_resposta(request):
    template_name = "manifestacao/detalhes/dados/resposta/inserir_resposta_body.html"

    try:
        texto_resposta = request.POST.get('resposta')
        is_resposta_conclusiva = request.POST.get('is_resposta_conclusiva') == 'on'
        id_manifestacao = request.POST.get('id_manifestacao')
        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        
        if not texto_resposta:
            return HttpResponse('É obrigatório informar uma resposta', status=401)

        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao) 
        movimentacao = gerar_movimentacao_inserir_resposta(gestor, manifestacao, texto_resposta, is_resposta_conclusiva)
        movimentacao.save()
        
        if is_resposta_conclusiva:
            manifestacao.resposta_conclusiva = texto_resposta
            status = get_object_or_404(Status, pk = Status.ID_ENCERRADA)
            manifestacao.status = status
        else:
            status = get_object_or_404(Status, pk = Status.ID_RESPOSTA_INTERMEDIARIA)
            manifestacao.status = status    
        
        manifestacao.save()
        manifestacao.movimentacoes.add(movimentacao)
        
        texto_movimentacao = 'Sua manifestação foi encerrada, acesse o sistema e consulte a resposta conclusiva informada.'
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Encerrada', texto_movimentacao)
        
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[INSERIR_RESPOSTA] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar inserir uma resposta', status=401)
   
    return render(request, template_name, context=locals())

def transferir_manifestacao(request):
    template_name = "manifestacao/detalhes/dados/ouvidoria_destino/ouvidoria_destino_body.html"
    try:
        manifestacao = None
        id_manifestacao = request.POST.get('id_manifestacao')
        id_ouvidoria_destino = request.POST.get('ouvidoria_destino')
        justificativa = request.POST.get('justificativa')
        
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        if id_ouvidoria_destino:
            ouvidoria_destino_novo = get_object_or_404(Orgao, pk = id_ouvidoria_destino)
            
        ouvidoria_antiga = manifestacao.ouvidoria_destino.get_nome_orgao()
         
        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        movimentacao_orgao_origem = gerar_movimentacao_ouvidoria_origem(gestor, manifestacao, ouvidoria_destino_novo, justificativa)
        movimentacao_orgao_destino = gerar_movimentacao_ouvidoria_destino(gestor, manifestacao, ouvidoria_destino_novo, justificativa)
        movimentacao_orgao_origem.save()
        movimentacao_orgao_destino.save()
        
        manifestacao.ouvidoria_destino = ouvidoria_destino_novo
        manifestacao.responsavel = None
        manifestacao.save()
        
        manifestacao.movimentacoes.add(movimentacao_orgao_origem)
        manifestacao.movimentacoes.add(movimentacao_orgao_destino)
        
        texto_movimentacao = 'A manifestação foi transferida de ouvidoria: '   + ouvidoria_antiga  + ' para ' + ouvidoria_destino_novo.get_nome_orgao()
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Transferência de Ouvidoria', texto_movimentacao)
        
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[TRANSFERIR_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar transferir o órgão destino', status=401)
    return render(request, template_name, context=locals())

def alterar_responsavel(request):
    template_name = "manifestacao/detalhes/responsavel/responsavel_body.html"

    try:
        manifestacao = None
        id_manifestacao = request.POST.get('id_manifestacao')
        id_gestor = request.POST.get('gestor')
        
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)

        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        gestor_novo = get_object_or_404(UsuarioOrgao, pk = id_gestor)
        
        movimentacao = gerar_movimentacao_alterar_responsavel(gestor, manifestacao, manifestacao.responsavel, gestor_novo)
        movimentacao.save()
        
        manifestacao.responsavel = gestor_novo
        manifestacao.save()
        gestor = get_gestor_by_id(request.user.id)
        is_permissao_avaliar = manifestacao.ouvidoria_destino == gestor.orgao
        manifestacao.movimentacoes.add(movimentacao)
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
    except Exception as e:
        logging.error('[ALTERAR_RESPONSAVEL] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar alterar o responsável da manifestação', status=401)
    return render(request, template_name, context=locals())
    
def alterar_tipo_manifestacao(request):
    template_name = "manifestacao/detalhes/dados/tipo_manifestacao/tipo_manifestacao_body.html"

    try:
        manifestacao = None
        id_manifestacao = request.POST.get('id_manifestacao')
        tipo_manifestacao = request.POST.get('tipo_manifestacao')
        
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)

        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        
        tipo_manifestacao_atual = get_tipo_manifestacao_choice_by_chave(manifestacao.tipo_manifestacao)
        tipo_manifestacao_novo = get_tipo_manifestacao_choice_by_chave(tipo_manifestacao)

        movimentacao = gerar_movimentacao_tipo_manifestacao(gestor, manifestacao, tipo_manifestacao_atual, tipo_manifestacao_novo)
        movimentacao.save()
        
        manifestacao.tipo_manifestacao = tipo_manifestacao
        manifestacao.save()
        manifestacao.movimentacoes.add(movimentacao)
        
        texto_movimentacao = 'O tipo da manifestação foi alterado de : '   + tipo_manifestacao_atual  + ' para ' + tipo_manifestacao_novo
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Tipo de Manifestação', texto_movimentacao)
        
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[ALTERAR_TIPO_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar alterar o tipo de manifestação', status=401)
    return render(request, template_name, context=locals())

def alterar_assunto(request):
    template_name = "manifestacao/detalhes/dados/assunto/assunto_body.html"

    try:
        manifestacao = None
        assunto = None
        id_manifestacao = request.POST.get('id_manifestacao')
        id_assunto = request.POST.get('assunto')
        
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        if id_assunto:
            assunto = get_object_or_404(Assunto, pk = id_assunto)
        
        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        assunto_antigo = manifestacao.assunto.assunto
        
        movimentacao = gerar_movimentacao_assunto(gestor, manifestacao, assunto.assunto)
        movimentacao.save()
        
        manifestacao.assunto = assunto
        manifestacao.movimentacoes.add(movimentacao)
        manifestacao.save()
        
        texto_movimentacao = 'O assunto da manifestação foi alterado de '+ assunto_antigo + ' para ' + assunto.assunto
        
        if manifestacao.cidadao:
            email.enviar_email_manifestacao_movimentacao(manifestacao.cidadao, manifestacao.numero_protocolo, 'Alteração no Assunto', texto_movimentacao)
        
        manifestacao_form = ManifestacaoDetalhesForm(instance=manifestacao)
        
    except Exception as e:
        logging.error('[ALTERAR_ASSUNTO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao tentar alterar o assunto', status=401)
    return render(request, template_name, context=locals())

def load_respostas_manifestacao(request, id_manifestacao):
    template_name = "manifestacao/detalhes/movimentacao/resposta/respostas_body.html"
    movimentacoes = None
    
    try:
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)
        
        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        movimentacoes = Movimentacao.objects.filter(manifestacao__id=id_manifestacao, orgao_origem=gestor.orgao).order_by('-data_cadastro')
        
        RESPOSTAS_ARRAY = [Movimentacao.CHAVE_RESPOSTA, Movimentacao.CHAVE_RESPOSTA_CONCLUSIVA]
        movimentacoes_respostas = movimentacoes.filter(tipo_alteracao__in=RESPOSTAS_ARRAY).order_by('-data_cadastro')
        
    except Exception as e:
        logging.error('[LOAD_RESPOSTAS_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao carregar as respostas', status=401)
    return render(request, template_name, context=locals())

def load_movimentacoes_manifestacao(request, id_manifestacao):
    template_name = "manifestacao/detalhes/movimentacao/timeline/manifestacao_timeline_body.html"
    movimentacoes = None
    
    try:
        if id_manifestacao:
            manifestacao = get_object_or_404(Manifestacao, pk = id_manifestacao)

        gestor = get_object_or_404(UsuarioOrgao, pk = request.user.id)
        movimentacoes = Movimentacao.objects.filter(manifestacao__id=id_manifestacao, orgao_origem=gestor.orgao).order_by('-data_cadastro')
        
    except Exception as e:
        logging.error('[LOAD_MOVIMENTACOES_MANIFESTACAO] - ' + str(e))
        return HttpResponse('Ocorreu um problema ao carregar as movimentações', status=401)
    return render(request, template_name, context=locals())