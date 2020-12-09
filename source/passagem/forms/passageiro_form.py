from django import forms
from passagem.model.passageiro import Passageiro




class PassageiroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       
        super(PassageiroForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['nome'].widget.attrs['style'] = 'text-transform: uppercase;'
        self.fields['cpf'].widget.attrs['class'] = 'form-control cpf'
        self.fields['data_nascimento'].widget.attrs['class'] = 'form-control date-picker'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['fone'].widget.attrs['class'] = 'form-control telefone'
        self.fields['categoria'].widget.attrs['class'] = 'form-control'
        self.fields['servidor'].widget.attrs['class'] = 'form-control'
        
    class Meta:
        model = Passageiro  
        fields = '__all__'
        

class PassageiroBuscarForm(forms.Form):
    cpf = forms.CharField(required=False)
    nome = forms.CharField(required=False)
    
    
    def __init__(self, *args, **kwargs):
        super(PassageiroBuscarForm, self).__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs['class'] = 'form-control cpf'
        self.fields['cpf'].widget.attrs['placeholder'] = 'Busque pelo o cpf'
        self.fields['nome'].widget.attrs['class'] = 'form-control'
       

            
        
#
                
    
        