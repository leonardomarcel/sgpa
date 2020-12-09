from django import forms
from manifestacao.models.manifestacao import Manifestacao
from manifestacao.models.assunto import Assunto
from basico.models.orgao import Orgao
from manifestacao.models.assunto_tipo import AssuntoTipo
from manifestacao.models.status import Status
from auth_local.util.enums import IDENTIFICACAO_CHOICES, TIPO_MANIFESTACAO_CHOICE, TIPO_MANIFESTACAO_AREA_RESTRITA_CHOICE, TIPO_ENTRADA_MANIFESTACAO
from auth_local.models.usuario_orgao import UsuarioOrgao
from manifestacao.models.manifestacao_tipo_presencial import ManifestacaoTipoPresencial

class ManifestacaoBuscarForm(forms.ModelForm):
    form_control_class = 'form-control '
    
    data_inicio = forms.DateTimeField(required=False)
    data_termino = forms.DateTimeField(required=False)
    numero_protocolo = forms.CharField(widget=forms.TextInput(), required=False)
    identificacao = forms.CharField(label="Manifestações", widget=forms.Select(choices=IDENTIFICACAO_CHOICES), required=False)
    tipo_manifestacao = forms.CharField(label="Tipo de Manifestação", widget=forms.Select(choices=TIPO_MANIFESTACAO_AREA_RESTRITA_CHOICE), required=False)
    status = forms.ModelChoiceField(Status.objects.all().order_by('id'), required=False)
    tipo_assunto = forms.ModelChoiceField(AssuntoTipo.objects.all().order_by('nome'), required=False)
    assunto = forms.ModelChoiceField(Assunto.objects.all().order_by('assunto'), required=False)
    ouvidoria_origem = forms.ModelChoiceField(Orgao.objects.all().order_by('sigla'), required=False)
    ouvidoria_destino = forms.ModelChoiceField(Orgao.objects.all().order_by('sigla'), required=False)
    gestor = forms.ModelChoiceField(UsuarioOrgao.objects.all().order_by('nome'), required=False)
    tipo_presencial = forms.ModelChoiceField(ManifestacaoTipoPresencial.objects.all().order_by('tipo'), required=False)
    tipo_entrada = forms.CharField(label="Tipo de Entrada", widget=forms.Select(choices=TIPO_ENTRADA_MANIFESTACAO), required=False)
            
    def __init__(self, *args, **kwargs):
        super(ManifestacaoBuscarForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.form_control_class
        
        if self.instance.orgao_razao and self.instance.orgao_razao.id:
            self.fields['gestor'].queryset= UsuarioOrgao.objects.filter(orgao=self.instance.orgao_razao)
            self.fields['gestor'].initial = self.instance.orgao_razao_id
            self.fields['ouvidoria_destino'].queryset = Orgao.objects.all()
        
        self.fields['status'].queryset = Status.objects.all().order_by('id').exclude(pk__in=[Status.ID_RESPOSTA_INTERMEDIARIA, Status.ID_ENCAMINHADA_OUVIDORIA_EXTERNA])
        self.fields['data_inicio'].widget.attrs['data-date-format'] = 'dd/mm/yyyy'
        self.fields['data_inicio'].widget.attrs['class'] = 'form-control date-picker'
        self.fields['data_termino'].widget.attrs['data-date-format'] = 'dd/mm/yyyy'
        self.fields['data_termino'].widget.attrs['class'] = 'form-control date-picker'
        
        
    class Meta:
        model = Manifestacao
        fields = '__all__'
        exclude = ('numero_protocolo', 'status', 'tipo_manifestacao', 'assunto', 'ouvidoria_destino', 'texto_manifestacao', 'movimentacoes', 'data_abertura', 'data_previsao_resposta', 'tipo_identificacao', 'anexos', 'anexos_cidadao')