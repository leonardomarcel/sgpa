from django import forms

class ManifestacaoArquivoForm(forms.Form):
    form_control_class = 'form-control '
    
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, **kwargs):
        super(ManifestacaoArquivoForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = self.form_control_class