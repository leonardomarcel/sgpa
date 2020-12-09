from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from passagem.views.manter_passageiro import PassageiroListView
from passagem.model.passageiro import Passageiro
from django.contrib.auth.models import User
from basico.models.orgao import Orgao

class PassageiroListViewTest(TestCase):
    """classe de testes de PassageiroListView """
    @classmethod
    def setUpTestData(cls):
        # criação de 13 passageiro para o teste de paginação
        numero_de_passageiros = 13
        cpfs =['111.111.111-11', '222.222.222-22', '333.333.333-33', '444.444.444-44', '555.555.555-55', '666.666.666-66', '777.777.777-77', '888.888.888-88', '999.999.999-99','015.081.820-35','840.869.590-89', '746.382.790-90', '015.968.980-54', '204.374.490-92']

        fones = ['(82)1111-1111', '(82)222-2222', '(82)3333-3333', '(82)4444-4444', '(82)5555-5555', '(82)6666-6666', '(82)7777-7777', '(82)8888-8888', '(82)9999-9999',  '(82)1010-1010', '(82)1111-1111', '(82)1212-1212', '(82)1313-1313', '(82)1414-1414']

        for passageiro_id in range(numero_de_passageiros):
            passageiro = Passageiro.objects.create(nome='nome_'.join(str(passageiro_id)), cpf=cpfs[passageiro_id], fone=fones[passageiro_id], email=str(passageiro_id).join('@mail.com'), servidor=True, categoria='is_adulto', data_nascimento='1984-08-23')
    
    def test_view_url_exists_at_desired_location(self):

      
        response = self.client.get('/passagem/passageiros/') 
        self.assertEquals(response.status_code, 200)

    def test_view_url_acessible_by_name(self):
        response = self.client.get(reverse('passagem:passageiros'))
        self.assertEquals(response.status_code, 200)

   
