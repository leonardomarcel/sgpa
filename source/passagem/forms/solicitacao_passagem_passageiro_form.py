from django import forms
from passagem.model.passageiro import Passageiro
from ckeditor import widgets
from django.forms.widgets import SelectMultiple

TIPO_CHOICE = (
                 ('I','IDA'),
                 ('IV','IDA E VOLTA'),
                 )

class SolicitacaoPassagemPassageiroForm(forms.Form):
    
    passageiros = forms.ModelMultipleChoiceField(queryset = Passageiro.objects.all(), widget=SelectMultiple())
    
    def __init__(self, *args, **kwargs):
       
        super(SolicitacaoPassagemPassageiroForm, self).__init__(*args, **kwargs)
        self.fields['passageiros'].widget.attrs['class'] = 'form-control  chosen-select multiple'
        #self.fields['passageiros'].widget.attrs['data-placeholder'] ='Selecione os passageiros'
        