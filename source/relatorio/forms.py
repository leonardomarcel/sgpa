from django import forms
from basico.models.orgao import Orgao
from passagem.model.agencia import Agencia
from passagem.model.motivo import Motivo
from passagem.model.companhia import Companhia
from passagem.model.passageiro import Passageiro

from auth_local.util.enums import IDENTIFICACAO_CHOICES, TIPO_MANIFESTACAO_CHOICE, TIPO_MANIFESTACAO_AREA_RESTRITA_CHOICE, TIPO_ENTRADA_MANIFESTACAO
from auth_local.models.usuario_orgao import UsuarioOrgao

class PassagemPeriodoForm(forms.Form):
    form_control_class = 'form-control '
    
    data_inicio = forms.DateTimeField(required=False)
    data_termino = forms.DateTimeField(required=False)
    orgao = forms.ModelChoiceField(Orgao.objects.all().order_by('sigla'), required=False)
    agencia_viagem = forms.ModelChoiceField(Agencia.objects.all().order_by('nome'), required=False)
    cia_aerea = forms.ModelChoiceField(Companhia.objects.all().order_by('nome'), required=False)
    motivo = forms.ModelChoiceField(Motivo.objects.all().order_by('nome'), required=False)
    passageiro = forms.ModelChoiceField(Passageiro.objects.all().order_by('nome'), required=False)
    urgente = forms.BooleanField(required=False)
        
    def __init__(self, *args, **kwargs):
        super(PassagemPeriodoForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.form_control_class
        
        self.fields['orgao'].widget.attrs['class'] = 'form-control  chosen-select'
        self.fields['agencia_viagem'].widget.attrs['class'] = 'form-control  chosen-select' 
        self.fields['cia_aerea'].widget.attrs['class'] = 'form-control  chosen-select'
        self.fields['motivo'].widget.attrs['class'] = 'form-control  chosen-select'   
        self.fields['passageiro'].widget.attrs['class'] = 'form-control  chosen-select'
        self.fields['data_inicio'].widget.attrs['data-date-format'] = 'dd/mm/yyyy'
        self.fields['data_inicio'].widget.attrs['class'] = 'form-control date-picker'
        self.fields['data_inicio'].widget.attrs['required'] = True
        self.fields['data_termino'].widget.attrs['data-date-format'] = 'dd/mm/yyyy'
        self.fields['data_termino'].widget.attrs['class'] = 'form-control date-picker'
        self.fields['data_termino'].widget.attrs['required'] = True
        
        
    