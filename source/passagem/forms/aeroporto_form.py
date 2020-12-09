from django import forms
from passagem.model.aeroporto import Aeroporto


class AeroportoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(AeroportoForm, self).__init__(*args, **kwargs)
        self.fields['cidade'].widget.attrs['class'] = 'form-control'
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['iata'].widget.attrs['class'] = 'form-control'
        self.fields['icao'].widget.attrs['class'] = 'form-control'
        self.fields['site'].widget.attrs['class'] = 'form-control'
        self.fields['latitude'].widget.attrs['class'] = 'form-control'
        self.fields['longitude'].widget.attrs['class'] = 'form-control'
        

    class Meta:
        model = Aeroporto
        fields = '__all__'
