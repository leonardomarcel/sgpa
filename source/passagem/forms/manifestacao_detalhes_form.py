from django import forms

from basico.models.orgao import Orgao
from manifestacao.models.manifestacao import Manifestacao
from manifestacao.models.assunto_tipo import AssuntoTipo
from auth_local.models.usuario_orgao import UsuarioOrgao
from auth_local.util.enums import TIPO_MANIFESTACAO_AREA_RESTRITA_CHOICE

class ManifestacaoDetalhesForm(forms.ModelForm):
    form_control_class = 'form-control '
    justificativa = forms.CharField(widget=forms.Textarea(attrs={ 'cols': 5, 'rows' : 5 }), required=False)
    complementacao = forms.CharField(widget=forms.Textarea(attrs={ 'cols': 5, 'rows' : 5 }), required=False)
    resposta = forms.CharField(widget=forms.Textarea(attrs={ 'cols': 5, 'rows' : 5 }), required=False)
    ouvidoria_destino = forms.ModelChoiceField(Orgao.objects.all().order_by('sigla'), required=False)
    tipo_assunto = forms.ModelChoiceField(AssuntoTipo.objects.all().order_by('nome'), required=False)
    tipo_manifestacao = forms.CharField(label="Tipo de Manifestação", widget=forms.Select(choices=TIPO_MANIFESTACAO_AREA_RESTRITA_CHOICE), required=False)
    gestor = forms.ModelChoiceField(UsuarioOrgao.objects.all().order_by('nome'), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ManifestacaoDetalhesForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.form_control_class
            
            self.fields['tipo_assunto'].initial  = self.instance.assunto.tipo.id
                        
        if self.instance.ouvidoria_destino:
            self.fields['gestor'].queryset= UsuarioOrgao.objects.filter(orgao=self.instance.ouvidoria_destino)
            self.fields['ouvidoria_destino'].queryset= UsuarioOrgao.objects.filter(orgao=self.instance.ouvidoria_destino)
            
        self.fields['ouvidoria_destino'].queryset = Orgao.objects.all().exclude(pk=self.instance.ouvidoria_destino.id)

        if self.instance.responsavel and self.instance.responsavel.id:
            self.fields['gestor'].initial = self.instance.responsavel.id
            
        
    class Meta:
        model = Manifestacao
        fields = '__all__'
        exclude = ('complementacao',  )