from django import forms
from auth_local.models.usuario_orgao import UsuarioOrgao
from auth_local.models.perfil import Perfil
from localflavor.br.forms import BRCPFField
from basico.models.orgao import Orgao
from passagem.model.solicitacao_passagem import SolicitacaoPassagem,\
    VIAGEM_SERVICO_CHOICE
from passagem.model.motivo import Motivo
from django.conf import settings
from passagem.model.acompanhamento_solicitacao_passagem import AcompanhamentoSolicitacaoPassagem



STATUS_CHOICE = (
                 ('TODAS','TODAS'),
                 ('ABERTA','ABERTA'),
                 ('COM PENDENCIA','COM PENDENCIA'),
                 ('AUTORIZADA','AUTORIZADA'),
                 )

class SolicitacaoPassagemForm(forms.ModelForm):
    
    
    #orgao = forms.ModelChoiceField(Orgao.objects.all(), required=True)
    #motivo = forms.ModelChoiceField(Motivo.objects.all(), required=True)
    anexos_processo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    viagem_servico = forms.ChoiceField(choices=VIAGEM_SERVICO_CHOICE) 
    #anexo_diario = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        super(SolicitacaoPassagemForm, self).__init__(*args, **kwargs)
        
        self.fields['motivo'].initial = Motivo.objects.get(pk=1)
        self.fields['anexo_diario'].widget.attrs['class'] = 'fas fa-file-pdf fa-2x text-danger'
        if not self.instance.pk:
            self.fields['anexos_processo'].widget.attrs['required'] = True

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

                  

   
    def clean_anexo_diario(self):
        arquivo_diario = self.cleaned_data['anexo_diario']
        if arquivo_diario:
            file_type = arquivo_diario.name.split('.')[-1]
            if file_type not in settings.TASK_UPLOAD_FILE_TYPES:
                raise forms.ValidationError( 'Enviar apenas aquivos .pdf, jpeg, jpg ou png.' )
            if file_type in settings.TASK_UPLOAD_FILE_TYPES and arquivo_diario.size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                raise forms.ValidationError( 'O tamanho do arquivo não pode ultrapassar 2.5 megabytes.' )
                        
        #except:
            #pass
        return arquivo_diario
                    
    class Meta:
        model = SolicitacaoPassagem  
        exclude = ('passagens', 'orgao', 'status', 'codigo', 'anexos_processo', )

class SolicitacaoPassagemBuscarForm(forms.Form):
    inicio = forms.DateField(required=False)
    termino = forms.DateField(required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICE)
    codigo = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(SolicitacaoPassagemBuscarForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget.attrs['class'] = 'form-control inicio date-picker'
        self.fields['termino'].widget.attrs['class'] = 'form-control termino date-picker'
        self.fields['codigo'].widget.attrs['class'] = 'form-control status'


class AcompanhamentoSolicitacaoPassagemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AcompanhamentoSolicitacaoPassagemForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs['class'] = 'form-control'
        self.fields['descricao'].widget.attrs['required'] = True
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['required'] = True
    
    class Meta:
        model = AcompanhamentoSolicitacaoPassagem  
        exclude = ('data', 'usuario', 'solicitacao_passagem')
        