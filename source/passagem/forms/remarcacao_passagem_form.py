from django import forms
from passagem.model.remarcacao_passagem import RemarcacaoPassagem




class RemarcacaoPassagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       
        super(RemarcacaoPassagemForm, self).__init__(*args, **kwargs)
        self.fields['valor'].widget.attrs['class'] = 'form-control'
        self.fields['valor_embarque'].widget.attrs['class'] = 'form-control'
        self.fields['tarifa'].widget.attrs['class'] = 'form-control'
        self.fields['multa'].widget.attrs['class'] = 'form-control'
        self.fields['num_voo'].widget.attrs['class'] = 'form-control'
        self.fields['num_bilhete'].widget.attrs['class'] = 'form-control'
        self.fields['taxa_servico'].widget.attrs['class'] = 'form-control'
        self.fields['data_viagem'].widget.attrs['class'] = 'form-control date-picker'
        
    class Meta:
        model = RemarcacaoPassagem  
        exclude = ('passageiro_passagem',)
        


       

            
        

                
    
        