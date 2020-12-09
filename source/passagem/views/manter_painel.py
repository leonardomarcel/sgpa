import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from auth_local.models.usuario_orgao import UsuarioOrgao
from util.util import is_recaptcha_success, get_gestor_by_id
from util.group_required_mixin import GroupRequiredMixin
from sgpa.settings.settings import LOGIN_URL

#@method_decorator(login_required, name=LOGIN_URL)
class PainelView(GroupRequiredMixin, TemplateView):
    template_name = "painel.html"
    #group_required = [UsuarioOrgao.GROUP_GESTOR_CGE, UsuarioBase.GROUP_AREA_RESTRITA]

    def get(self, request):
        gestor = get_gestor_by_id(self.request.user.id)

        #manifestacoes = Manifestacao.objects.filter(ouvidoria_destino=gestor.orgao).distinct()
        year = datetime.datetime.today().year
        
       
        
        #total_manifestacao = manifestacoes.count()
        
        #manifestacao_count = manifestacoes.values('tipo_manifestacao').annotate(quantidade=Count('id'))
        #manifestacao_status_count = manifestacoes.values('status').annotate(quantidade=Count('id'))
       # manifestacoes_dict = { manifestacao['tipo_manifestacao']: manifestacao['quantidade'] for manifestacao in manifestacao_count }
       # manifestacoes_status_dict = { manifestacao['status']: manifestacao['quantidade'] for manifestacao in manifestacao_status_count }

        #statistics_manifestacoes = StatisticManifestacaoOrgao.objects.filter(orgao_id=gestor.orgao.id)
        #months_count = [month.month_count for month in statistics_manifestacoes]
        #months_name = [month.month_number for month in statistics_manifestacoes]
        
        #total_denuncia = manifestacoes_dict.get('denuncia', 0)
        #total_reclamacao = manifestacoes_dict.get('reclamacao', 0)
        #total_solicitacao = manifestacoes_dict.get('solicitacao', 0)
        #total_sugestao = manifestacoes_dict.get('sugestao', 0)
        #total_elogio = manifestacoes_dict.get('elogio', 0)
        #total_fora_escopo = manifestacoes_dict.get('fora-escopo', 0)
            
        return render(request, self.template_name, context=locals())

class EsqueceuSuaSenhaGestorView(TemplateView):
    template_name = "esqueceu_sua_senha_gestor.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        if is_recaptcha_success(recaptcha_response):
            cpf = request.POST.get('cpf_redefinicao')
            
            if not cpf:
                messages.error(request, 'É obrigatório informar o Login (CPF).')
                return render(request, self.template_name)
            else:
                try:
                    gestor = UsuarioOrgao.objects.get(cpf=cpf)
                    gestor.save_new_password_generate()
                    
                    username = gestor.email.split('@')[0]
                    username = username[:3]
                    domain = gestor.email.split('@')[1]
                    email = username + '*****@'+ domain

                    messages.success(request, 'Uma nova senha foi enviada para <strong>' + email + '</strong>')
                except UsuarioOrgao.DoesNotExist:
                    gestor = None
                    messages.error(request, 'Não foi encontrado nenhum usuário com o CPF informado.')
                    return render(request, self.template_name)
        else:
            messages.error(request, 'É obrigatório marcar o <strong>reCAPTCHA</strong>.')
            return render(request, self.template_name)
        
        return redirect('login_gestor')        
