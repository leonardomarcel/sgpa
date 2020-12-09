from django.http import JsonResponse
from django.views import View

from basico.models.municipio import Municipio

class Cidade(View):
    model = Municipio
    
    def get(self, request, estado_id):
        cidades_dict = []
        
        for cidade in self.model.objects.filter(estado__pk=estado_id):
            cidades_dict.append({'id': cidade.id,
                                'nome': cidade.nome,
                                'estado_nome' : cidade.estado.nome,
                                'estado_sigla' : cidade.estado.sigla
                                })
        return JsonResponse(cidades_dict, safe=False)