from django import forms
from django.contrib.auth import authenticate

from auth_local.models.usuario_orgao import UsuarioOrgao

class GestorPasswordForm(forms.ModelForm):
    error_css_class = 'is-invalid '
    success_css_class = 'is-valid '
    form_control_class = 'form-control '
    selectize_class = 'selectize '
    msg_campo_obrigatorio = 'Este campo é obrigatório.'

    senha_atual = forms.CharField(max_length=32, widget=forms.PasswordInput, required = False)
    nova_senha = forms.CharField(max_length=32, widget=forms.PasswordInput, required = False)
    confirmar_senha = forms.CharField(max_length=32, widget=forms.PasswordInput, required = False)
    
    def __init__(self, *args, **kwargs):
        self._usuario = kwargs.pop('usuario')
        super(GestorPasswordForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs['value'] = self._usuario.nome
        
        if self._usuario.telefone:
            self.fields['telefone'].widget.attrs['value'] = self._usuario.telefone 
            
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        self.fields['telefone'].widget.attrs['class'] = 'form-control telefone'
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome:
            self._errors['nome'] = self.error_class([self.msg_campo_obrigatorio])
            self.fields['nome'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        else:
            self.fields['nome'].widget.attrs['class'] = self.success_css_class + self.form_control_class
            return nome
        
    def clean_senha_atual(self):
        senha_atual = self.cleaned_data.get('senha_atual')
        email = self._usuario.email
        
        if senha_atual and not authenticate(username=email, password=senha_atual):
            self._errors['senha_atual'] = self.error_class(['A senha atual está incorreta.'])
            self.fields['senha_atual'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        return senha_atual

    def clean_confirmar_senha(self):
        nova_senha = self.cleaned_data.get('nova_senha')
        confirmacao_nova_senha = self.cleaned_data.get('confirmar_senha')
        
        if nova_senha and len(nova_senha) < 6:
            self._errors['nova_senha'] = self.error_class(['Informe uma senha com no mínimo 06 caracteres.'])
        
        if confirmacao_nova_senha and len(confirmacao_nova_senha) < 6:
            self._errors['confirmar_senha'] = self.error_class(['Informe uma senha com no mínimo 06 caracteres.'])
        
        if nova_senha != confirmacao_nova_senha:
            self._errors['nova_senha'] = self.error_class(['As novas senhas fornecidas são diferentes.'])
            self._errors['confirmar_senha'] = self.error_class(['As novas senhas fornecidas são diferentes.'])
            self.fields['senha_atual'].widget.attrs['class'] = self.error_css_class + self.form_control_class
            self.fields['confirmar_senha'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        return nova_senha

    class Meta:
        model = UsuarioOrgao   
        fields = '__all__'
        exclude = ('cpf','orgao', 'perfil', 'email', 'password')