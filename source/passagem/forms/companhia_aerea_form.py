from django import forms
from passagem.model.companhia import Companhia


class CompanhiaAereaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(CompanhiaAereaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['iata'].widget.attrs['class'] = 'form-control'
        self.fields['icao'].widget.attrs['class'] = 'form-control'
        self.fields['site'].widget.attrs['class'] = 'form-control'
        self.fields['fone'].widget.attrs['class'] = 'form-control telefone'
        self.fields['fax'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        

    class Meta:
        model = Companhia
        fields = '__all__'
