from django import forms
from passagem.model.cotacao import Cotacao

class CotacaoPassagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CotacaoPassagemForm, self).__init__(*args, **kwargs)
        self.fields['numero_voo'].widget.attrs['class'] = 'form-control'
        self.fields['valor'].widget.attrs['class'] = 'form-control'
        self.fields['companhia'].widget.attrs['class'] = 'form-control'
        self.fields['data'].widget.attrs['class'] = 'form-control datetimepicker5'
        
    class Meta:
        model = Cotacao  
        exclude = ('passagem',)
        


    
    
    
            
        

                
    
        