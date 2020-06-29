from django import forms
from auth_local.models.usuario_orgao import UsuarioOrgao
from auth_local.models.perfil import Perfil
from localflavor.br.forms import BRCPFField
from basico.models.orgao import Orgao

class GestorForm(forms.ModelForm):
    error_css_class = 'is-invalid '
    success_css_class = 'is-valid '
    form_control_class = 'form-control '
    selectize_class = 'selectize '
    msg_campo_obrigatorio = 'Este campo é obrigatório.'
    
    orgao = forms.ModelChoiceField(Orgao.objects.all(), required=True)
    perfil = forms.ModelChoiceField(label="Perfil", queryset=Perfil.objects.filter(pk__in=[1,2,3,4]), required=False)
    cpf = BRCPFField(max_length = 14, min_length = 1, error_messages = { 'invalid': 'Número do CPF inválido.', 'max_digits': 'Este campo requer no máximo 11 dígitos ou 14 caracteres.' })
    
    def __init__(self, *args, **kwargs):
        super(GestorForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].required = False
        
        self.fields['cpf'].widget.attrs['class'] = 'form-control cpf'
        self.fields['telefone'].widget.attrs['class'] = 'form-control telefone'
        
        if self.instance.id:
            if self.instance.orgao:
                self.fields['orgao'].initial  = self.instance.orgao.id
    
    def clean_perfil(self):
        perfil = self.cleaned_data.get('perfil')
        
        if not perfil:
            self._errors['perfil'] = self.error_class([self.msg_campo_obrigatorio])
            self.fields['perfil'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        else:
            self.fields['perfil'].widget.attrs['class'] = self.success_css_class + self.form_control_class
            return perfil
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        msg_cpf_exists = 'O CPF informado já existe.'
        
        if not cpf:
            self._errors['cpf'] = self.error_class([self.msg_campo_obrigatorio])
            self.fields['cpf'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        else:
            if self.instance.id:
                if not self.instance.cpf == cpf:
                    if UsuarioOrgao.objects.filter(cpf=cpf):
                        self._errors['cpf'] = self.error_class([msg_cpf_exists])
                        return cpf
            else:
                if UsuarioOrgao.objects.filter(cpf=cpf):
                    self._errors['cpf'] = self.error_class([msg_cpf_exists])
                    return cpf
            self.fields['cpf'].widget.attrs['class'] = self.success_css_class + self.form_control_class
            return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        msg_email_exists = 'O e-mail informado já existe.'
        if not email:
            self._errors['email'] = self.error_class([self.msg_campo_obrigatorio])
            self.fields['email'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        else:
            if self.instance.id:
                if not self.instance.email == email:
                    if UsuarioOrgao.objects.filter(email=email):
                        self._errors['email'] = self.error_class([msg_email_exists])
                        return email
            else:
                if UsuarioOrgao.objects.filter(email=email):
                    self._errors['email'] = self.error_class([msg_email_exists])
                    return email
                    
            self.fields['email'].widget.attrs['class'] = self.success_css_class + self.form_control_class
            return email
        
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if not nome:
            self._errors['nome'] = self.error_class([self.msg_campo_obrigatorio])
            self.fields['nome'].widget.attrs['class'] = self.error_css_class + self.form_control_class
        else:
            self.fields['nome'].widget.attrs['class'] = self.success_css_class + self.form_control_class
            return nome
    
    class Meta:
        model = UsuarioOrgao  
        fields = '__all__'
        exclude = ('password', 'orgao')