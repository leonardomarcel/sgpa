from django import forms
from passagem.model.passageiro_passagem import PassageiroPassagem

class PassageiroPassagemForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        super(PassageiroPassagemForm, self).__init__(*args, **kwargs)
        self.fields['num_bilhete'].widget.attrs['class'] = 'form-control'
        self.fields['num_bilhete'].required = True
        self.fields['num_voo'].widget.attrs['class'] = 'form-control'
        self.fields['num_voo'].required = True
        self.fields['companhia'].widget.attrs['class'] = 'form-control'
        self.fields['companhia'].required = True
        self.fields['tarifa'].widget.attrs['class'] = 'form-control'
        self.fields['tarifa'].required = True
        self.fields['valor'].widget.attrs['class'] = 'form-control'
        self.fields['valor'].required = True
        self.fields['valor_embarque'].widget.attrs['class'] = 'form-control'
        self.fields['valor_embarque'].required = True
        self.fields['taxa_servico'].widget.attrs['class'] = 'form-control'
        self.fields['data_viagem'].widget.attrs['class'] = 'form-control datetimepicker5'
        self.fields['taxa_servico'].required = True
        
        
    class Meta:
        model = PassageiroPassagem  
        exclude = ('passagem', 'passageiro', 'status')
        


    
        