from django import forms

class RelatorioPrintManifestacaoForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(RelatorioPrintManifestacaoForm, self).__init__(*args, **kwargs)

