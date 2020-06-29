from django.urls import path


from basico.views.manter_cidade import Cidade
app_name = 'basico' 

urlpatterns = [
    path('cidades_json/<int:estado_id>/', Cidade.as_view(), name='listar_cidades_json'),
]
