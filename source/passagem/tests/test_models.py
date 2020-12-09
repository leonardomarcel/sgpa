from django.test import  TestCase
from passagem.model.passageiro import Passageiro
from datetime import date

class PassageiroModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """ metodo de de criação de um objeto para ser usado por todos
            os metodos de testes dessa classe"""
        Passageiro.objects.create(nome='Leonardo Marcel', cpf='111.111.111-11', fone='(82)98988-84848', 
                                  email='leonardo@mail.com', servidor=True, categoria='is_adulto', 
                                  data_nascimento='1984-12-08')
    
    def test_data_nascimento_label(self):
        passageiro = Passageiro.objects.get(id=1)
        field_label = passageiro._meta.get_field('data_nascimento').verbose_name
        self.assertEquals(field_label, 'data nascimento')
    
    def str_method_return(self):
        passageiro = Passageiro.objects.get(pk=1)
        retono_esperado = f'{passageiro.cpf}, {passageiro.nome}'
        self.assertEquals(retono_esperado, str(passageiro))
        
    def verifica_ano_nacimento(self):
        """teste para verificar se o método idade está retonando o valor correto"""
        
        passageiro = Passageiro.objects.get(pk=1)

        if (date.today().month < passageiro.data_nascimento.month) or\
            (date.today().month == passageiro.data_nascimento.month and  date.today().day < passageiro.data_nascimento.day):
            idade =  date.today().year - passageiro.data_nascimento.year
            idade = idade - 1
            self.assertEquals(idade, passageiro.idade())  
        if (date.today().month > passageiro.data_nascimento.month) or\
            (date.today().month == passageiro.data_nascimento.month and  date.today().day >= passageiro.data_nascimento.day):
            idade =  date.today().year - passageiro.data_nascimento.year
            self.assertEquals(idade, passageiro.idade()) 
            

