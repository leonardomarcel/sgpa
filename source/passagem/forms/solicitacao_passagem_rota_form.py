from django import forms
from datetime import date
from passagem.model.aeroporto import Aeroporto
from passagem.model.passageiro import Passageiro
from django.forms.widgets import SelectMultiple
from passagem.model.rota import Rota
from passagem.model.cota import Cota
from datetime import timedelta
from django.utils.safestring import mark_safe

TIPO_CHOICE = (
                 ('I','IDA'),
                 ('IV','IDA E VOLTA'),
                 )


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
        cota = Cota.objects.get(orgao=orgao, exercicio=date.today().year)
    except:
        pass
    if cota:
        quantidade = cota.quantidade
    return quantidade

class SolicitacaoPassagemRotaForm(forms.Form):

    tipo = forms.ChoiceField(choices=TIPO_CHOICE) 
    origem = forms.ModelChoiceField(queryset = Aeroporto.objects.all(), required=False)
    destino = forms.ModelChoiceField(queryset = Aeroporto.objects.all(), required=False)
    data_ida = forms.DateField(required=False)
    data_volta = forms.DateField(required=False)
    passageiros = forms.ModelMultipleChoiceField(queryset = Passageiro.objects.all(), widget=SelectMultiple(), required=False)
    
    def __init__(self, *args, **kwargs):
        self.orgao = kwargs.pop('orgao')
        super(SolicitacaoPassagemRotaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['class'] = 'form-control tipo'
        self.fields['origem'].widget.attrs['class'] = 'form-control  chosen-select '
        self.fields['destino'].widget.attrs['class'] = 'form-control chosen-select'
        self.fields['data_ida'].widget.attrs['class'] = 'form-control data_ida date-picker'
        self.fields['data_volta'].widget.attrs['class'] = 'form-control data_volta date-picker'
        self.fields['passageiros'].widget.attrs['class'] = 'form-control  chosen-select multiple'


    # verificação para saber se o campo justificativa da urgência deve ser preenchido ou não (considerando somente dias úteis "seg a sex")
        

    def clean(self,  **kwargs):
        cleaned_data = super(SolicitacaoPassagemRotaForm, self).clean()
        tipo = cleaned_data.get('tipo')
        origem   = cleaned_data.get('origem')
        destino  = cleaned_data.get('destino')
        passageiros = cleaned_data.get('passageiros')
        data_ida  = cleaned_data.get('data_ida')
        data_volta  = cleaned_data.get('data_volta')
        cota_quantidade = verifica_quantidade_cota(self.orgao)
        rota_ida = Rota.objects.filter(origem=origem, destino=destino)
        rota_volta = Rota.objects.filter(origem=destino, destino=origem)

        if not origem:
            self._errors['origem'] = self.error_class(['Campo obrigatório'])
        if not destino:
            self._errors['destino'] = self.error_class(['Campo obrigatório'])
        if not passageiros:
            self._errors['passageiros'] = self.error_class(['Campo obrigatório']) 
        if tipo == 'IV' and not data_volta:
            self._errors['data_volta'] = self.error_class(['Campo obrigatório'])
        
        if tipo == 'I' and origem and destino and not rota_ida :
            self.add_error(None, ' #Rota de ida inexistente.')
        if tipo == 'IV' and origem and destino and not rota_ida:
            self.add_error(None, ' #Rota de ida inexistente.')
        if tipo == 'IV' and origem and destino and not rota_volta:
            self.add_error(None, ' #Rota de volta inexistente.')
        if passageiros and tipo == 'I' and cota_quantidade < len(passageiros):
            self.add_error(None, ' #Você não tem mais cota para solicitar passagem! Entre em contato com a Gestão de Passagens Aéreas da AMGESP.')
        if passageiros and tipo == "IV" and cota_quantidade < len(passageiros) * 2:
            self.add_error(None, ' #Você não tem mais cota para solicitar passagem! Entre em contato com a Gestão de Passagens Aéreas da AMGESP.')
        if tipo == "IV" and  data_volta and data_ida > data_volta:
            self.add_error(None, ' #A data de ida informada é maior que a data de volta.')
        if data_ida and data_ida < date.today():
            self.add_error(None, ' #A data de ida informada é menor que a data atual.')
        
        return cleaned_data
    
    
    
    # def clean_data_ida(self):
    #     data_ida = self.cleaned_data['data_ida']
    #     if not data_ida:
    #         self._errors['data_ida'] = self.error_class(['Campo obrigatóriooooo'])
    #     lista_dias = (0,1,2,3,4)
    #     contador = 0
    #     if data_ida:
    #         dias = (data_ida - date.today()).days   
    #         for i in range(dias):
    #             data_solic = date.today()
    #             prox_dia = data_solic + timedelta(days=i)
                
    #             if prox_dia.weekday() in lista_dias:                    
    #                 contador+=1                   
    #                 #data_solic = data_solic+timedelta(days=1)                                
    #         if contador<5: 
    #             #msg = 'solicitação de passagem fora do prazo mínimo de 05 (dias úteis seg a sexta) dias úteis. Clique aqui para justificar:'
    #             self.add_error(None, 'solicitação de passagem fora do prazo mínimo de 05 dias úteis.  '+ mark_safe('<a href="" data-toggle="modal" data-target="#modalLoginForm" >Clique para justificar</a>'))
    #     return data_ida
            
#     def clean_data_ida(self):
#         data_ida = self.cleaned_data.get('data_ida')
#         msg = 'Data inválida.'
#         if data_ida < date.today():  
#             self._errors['data_ida'] = self.error_class([msg])      
#         
        