# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.context import Context
from django.template.loader import get_template

def send_email(usuario, titulo, contexto, template_html, template_plain ):
    texto_contexto = template_plain.render(contexto)
    msg = EmailMultiAlternatives(titulo, texto_contexto,
                                 'suportesistemas.itec@itec.al.gov.br',
                                 [usuario.email])
    msg.send()
    

def enviar_confirmacao_nova_senha(usuario, token):
    template_plain = get_template('email/reset_password_confirmation.txt')
    url_confirmar = settings.SITE_URL + "confirmar_nova_senha/?token=" + token.hash
    url_cancelar = settings.SITE_URL + "cancelar_nova_senha/?token=" + token.hash
    context = Context({"link_confirmar": url_confirmar,
                       "link_cancelar": url_cancelar,
                       "name": usuario.get_full_name() })
    send_email(usuario, u"Sistema de Passaens Aéreas - Email de Confirmação Nova Senha",
               context, None, template_plain)
    
def enviar_email_nova_senha(usuario, nova_senha):
    template_plain = get_template('email/reset_password.txt')
    contexto = Context({"nova_senha": nova_senha})
    send_email(usuario, u"Sistema de Passagens Aéreas - Nova Senha",
               contexto, None, template_plain)