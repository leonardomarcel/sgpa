from django import forms
from auth_local.models.usuario_orgao import UsuarioOrgao
from basico.models.orgao import Orgao
from auth_local.models.perfil import Perfil
from auth_local.util.enums import GESTOR_STATUS
from localflavor.br.forms import BRCPFField

class UsuarioBuscarForm(forms.ModelForm):
    form_control_class = 'form-control '
    
    nome = forms.CharField(widget=forms.TextInput(), required=False)
    perfil = forms.ModelChoiceField(Perfil.objects.all().order_by('nome'), required=False)
    ouvidoria = forms.ModelChoiceField(Orgao.objects.all().order_by('descricao'), required=False)
    status = forms.CharField(label="Status", widget=forms.Select(choices=GESTOR_STATUS), required=False)
    cpf = BRCPFField(max_length = 14, min_length = 1, error_messages = { 'invalid': 'Número do CPF inválido.', 'max_digits': 'Este campo requer no máximo 11 dígitos ou 14 caracteres.' }, required=False)

    def __init__(self, *args, **kwargs):
        super(UsuarioBuscarForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.form_control_class
        
        self.fields['cpf'].widget.attrs['class'] = 'form-control cpf'
        
    class Meta:
        model = UsuarioOrgao
        fields = '__all__'
        exclude = ('password', 'nome', 'email', 'orgao')