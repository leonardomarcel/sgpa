from django import forms
from auth_local.models.usuario_cidadao import UsuarioCidadao

class CidadaoBuscarForm(forms.ModelForm):
    form_control_class = 'form-control '
    
    nome = forms.CharField(widget=forms.TextInput(), required=False)
        
    def __init__(self, *args, **kwargs):
        super(CidadaoBuscarForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.form_control_class
        
    class Meta:
        model = UsuarioCidadao
        fields = '__all__'
        exclude = ('cpf', 'password', 'email', )