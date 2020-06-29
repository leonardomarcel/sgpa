from django import forms
from passagem.model.rota import Rota


class RotaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(RotaForm, self).__init__(*args, **kwargs)
        self.fields['origem'].widget.attrs['class'] = 'form-control'
        self.fields['destino'].widget.attrs['class'] = 'form-control'
       
        

    class Meta:
        model = Rota
        fields = '__all__'
