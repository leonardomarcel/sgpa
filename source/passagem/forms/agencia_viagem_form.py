from django import forms
from passagem.model.agencia import Agencia




class AgenciaViagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(AgenciaViagemForm, self).__init__(*args, **kwargs)

        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['cnpj'].widget.attrs['class'] = 'form-control'
        self.fields['inscricao_estadual'].widget.attrs['class'] = 'form-control'
        self.fields['nome_fantasia'].widget.attrs['class'] = 'form-control'
        self.fields['contrato'].widget.attrs['class'] = 'form-control'
        self.fields['fone'].widget.attrs['class'] = 'form-control telefone'
        self.fields['fax'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['homepage'].widget.attrs['class'] = 'form-control'
        

    class Meta:
        model = Agencia
        fields = '__all__'
