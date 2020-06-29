from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.conf import settings
from datetime import datetime
#from passagem.model.passagem import Passagem

def enviar_email_nova_senha_cidadao(usuario, nova_senha):
    template_html = get_template('email/cidadao/email_senha_cidadao.html')

    contexto = {
        "nome_sistema": settings.NOME_E_OUV_ALAGOAS,
        "email_rodape": settings.EMAIL_NOME_E_OUV_ALAGOAS_COMPLETO,
        "assunto": settings.EMAIL_ASSUNTO_REDEFINICAO_SENHA,
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "url_site": settings.EMAIL_URL_SITE_HOMOLOGACAO if settings.IS_HOMOLOGACAO else settings.EMAIL_URL_SITE_PRODUCAO,
        "email_usuario": usuario.email,
        "nome_usuario": usuario.nome,
        "nova_senha": nova_senha
    }
    
    if not usuario.is_cidadao():
        contexto['cpf_usuario'] = usuario.cpf

    email = EmailMultiAlternatives(settings.EMAIL_NOME_E_OUV_ALAGOAS, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('email/cidadao/email_senha_cidadao.html', contexto)
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
    except:
        pass

def enviar_email_nova_senha_gestor(usuario, nova_senha):
    template_html = get_template('email/gestor/email_senha_gestor.html')
    contexto = {
            "nome_sistema": settings.NOME_SGPA,
            "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
            "assunto": settings.EMAIL_ASSUNTO_REDEFINICAO_SENHA,
            "url_logo": settings.EMAIL_URL_LOGO_ITEC,
            #"url_site": settings.EMAIL_URL_SITE_HOMOLOGACAO if settings.IS_HOMOLOGACAO else settings.EMAIL_URL_SITE_PRODUCAO,
            "email_usuario": usuario.email,
            "cpf_usuario": usuario.cpf,
            "nome_usuario": usuario.nome,
            "nova_senha": nova_senha
        }
    
    email = EmailMultiAlternatives(settings.EMAIL_NOME_SGPA_ALAGOAS, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('email/gestor/email_senha_gestor.html', contexto)
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
    except:
        return False
    return True

def enviar_email_solicitacao_passagem_criada(usuario, solicitacao_passagem, passagens):
    template_html = get_template('solicitacao_passagem/email/solicitacao_passagem_criada.html')
    

    contexto = {
        "nome_sistema": "SGPA Alagoas",
        "solicitacao_passagem": solicitacao_passagem,
        "passagens": passagens,
        "data": datetime.now(),
        "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
        "assunto": "SGPA Alagoas - Solicitação de Passagem Criada",
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "email_usuario": usuario.email,
        "cpf_usuario": usuario.cpf,
        "nome_usuario": usuario.nome

    }
    email = EmailMultiAlternatives(settings.EMAIL_TITLE_SOLICITACAO_PASSAGEM, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('solicitacao_passagem/email/solicitacao_passagem_criada.html', contexto)
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
    except:
        return False
    return True

def enviar_email_solicitacao_passagem_editada(usuario, solicitacao_passagem, passagens):
    template_html = get_template('solicitacao_passagem/email/solicitacao_passagem_criada.html')

    contexto = {
        "nome_sistema": "SGPA Alagoas",
        "solicitacao_passagem": solicitacao_passagem,
        "passagens": passagens,
        "data": datetime.now(),
        "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
        "assunto": "SGPA Alagoas - Solicitação de Passagem Editada",
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "email_usuario": usuario.email,
        "cpf_usuario": usuario.cpf,
        "nome_usuario": usuario.nome

    }
    email = EmailMultiAlternatives(settings.EMAIL_TITLE_SOLICITACAO_PASSAGEM, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('solicitacao_passagem/email/solicitacao_passagem_criada.html', contexto)
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
    except:
        return False
    return True

def enviar_email_solicitacao_passagem_aprovada(usuario, solicitacao_passagem, passagens):

    template_html = get_template('solicitacao_passagem/email/solicitacao_passagem_aprovada.html')
    
    contexto = {
        "nome_sistema": "SGPA Alagoas",
        "passagens": passagens,
        "codigo": solicitacao_passagem.codigo,
        "data": datetime.now(),
        "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
        "assunto": "SGPA Alagoas - Solicitação de Passagem Aprovada",
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "email_usuario": usuario.email,
        "cpf_usuario": usuario.cpf,
        "nome_usuario": usuario.nome

    }
    email = EmailMultiAlternatives(settings.EMAIL_TITLE_SOLICITACAO_PASSAGEM_APROVADA, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('solicitacao_passagem/email/solicitacao_passagem_aprovada.html', contexto)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
    except:
        return False
    return True

def enviar_email_solicitacao_passagem_reprovada(usuario, acompanhamento_solicitacao_passagem):

    template_html = get_template('solicitacao_passagem/email/solicitacao_passagem_reprovada.html')
    
    contexto = {
        "nome_sistema": "SGPA Alagoas",
        'acompanhamento': acompanhamento_solicitacao_passagem.descricao,
        'codigo': acompanhamento_solicitacao_passagem.solicitacao_passagem.codigo,
        "data": datetime.now(),
        "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
        "assunto": "SGPA Alagoas - Solicitação de Passagem Reprovada",
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "email_usuario": usuario.email,
        "cpf_usuario": usuario.cpf,
        "nome_usuario": usuario.nome

    }
    email = EmailMultiAlternatives(settings.EMAIL_TITLE_SOLICITACAO_PASSAGEM_REPROVADA, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('solicitacao_passagem/email/solicitacao_passagem_reprovada.html', contexto)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
    except:
        return False
    return True


def enviar_email_passagens_emitida(usuario, passageiro_passagem):
    template_html = get_template('passagem/email/passagem_emitida.html')

    contexto = {
        "nome_sistema": "SGPA Alagoas",
        "passageiro_passagem": passageiro_passagem,
        "data": datetime.now(),
        "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
        "assunto": "SGPA Alagoas - Passagem Emitida",
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "email_usuario": usuario.email,
        "cpf_usuario": usuario.cpf,
        "nome_usuario": usuario.nome

    }
    email = EmailMultiAlternatives(settings.EMAIL_TITLE_PASSAGEM_EMITIDA, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('passagem/email/passagem_emitida.html', contexto)
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
    except:
        return False
    return True

def enviar_email_passagem_remarcada(usuario, remarcacao_passagem):
    template_html = get_template('passagem/email/passagem_remarcada.html')
    
    contexto = {
        "nome_sistema": "SGPA Alagoas",
        'remarcacao': remarcacao_passagem,
        "data": datetime.now(),
        "email_rodape": settings.EMAIL_NOME_SGPA_ALAGOAS_COMPLETO,
        "assunto": "SGPA Alagoas - Passagem Remarcada",
        "url_logo": settings.EMAIL_URL_LOGO_ITEC,
        "email_usuario": usuario.email,
        "cpf_usuario": usuario.cpf,
        "nome_usuario": usuario.nome

    }
    email = EmailMultiAlternatives(settings.EMAIL_TITLE_PASSAGEM_REMARCADA, template_html.render(contexto), settings.DEFAULT_EMAIL_FROM, [usuario.email])
    
    html_content = render_to_string('passagem/email/passagem_remarcada.html', contexto)
    email.attach_alternative(html_content, "text/html")

    try:
        email.send()
    except:
        return False
    return True

# def enviar_email_manifestacao_movimentacao(cidadao, numero_protocolo, tipo_alteracao, texto_movimentacao):
#     template_html = get_template('email/cidadao/email_movimentacao_manifestacao.html')
#     nome_sistema = "e-Ouv Alagoas"
#     assunto = " Manifestação - " + numero_protocolo
#     email_rodape = settings.EMAIL_FOOTER_NOME_CGE

#     contexto = {
#                 "nome_sistema": nome_sistema,
#                 "email_rodape": email_rodape,
#                 "assunto": assunto,
#                 "url_logo": settings.EMAIL_URL_LOGO_ITEC,
#                 "email_usuario": cidadao.email,
#                 "numero_protocolo": numero_protocolo,
#                 "nome_cidadao": cidadao.nome,
#                 "texto_movimentacao": texto_movimentacao,
#                 "url_site": settings.EMAIL_URL_SITE_HOMOLOGACAO if settings.IS_HOMOLOGACAO else settings.EMAIL_URL_SITE_PRODUCAO
#                 }
    
#     send_movimentacao(cidadao.email, "e-Ouv Alagoas - Sua manifestação foi atualizada", contexto, template_html)
    
# def send_movimentacao(email_destinatario, titulo, contexto, template_html):
#     email = EmailMultiAlternatives(titulo, template_html.render(contexto), 'suportesistemas.itec@itec.al.gov.br', [email_destinatario])
#     html_content = render_to_string('email/cidadao/email_movimentacao_manifestacao.html', contexto)
#     email.attach_alternative(html_content, "text/html")
#     email.send()