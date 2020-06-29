from django import forms
from passagem.model.cota import Cota


class CotaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(CotaForm, self).__init__(*args, **kwargs)
        self.fields['orgao'].widget.attrs['class'] = 'form-control'
        self.fields['quantidade'].widget.attrs['class'] = 'form-control'
        self.fields['exercicio'].widget.attrs['class'] = 'form-control'
        self.fields['exercicio'].widget.attrs['class'] = 'form-control'
        self.fields['inicio'].widget.attrs['class'] = 'form-control date-picker'
        self.fields['termino'].widget.attrs['class'] = 'form-control date-picker'
        

    class Meta:
        model = Cota
        exclude = ('usuario_criacao', )
