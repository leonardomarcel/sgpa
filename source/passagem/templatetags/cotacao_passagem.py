# -*- coding: utf-8 -*-
u"""."""

from django import template
from passagem.model.passagem import Passagem
from passagem.model.cotacao import Cotacao
import json

register = template.Library()

@register.filter(name='cotacao_passagem')
def cotacao_passagem(id_passagem):
    try:
        passagem = Passagem.objects.get(pk=id_passagem)
        passageiros = passagem.passageiros.all()
        lista = []
        for passageiro in passageiros:
            dict_passageiros = {}
            dict_passageiros['nome']=passageiro.nome
            dict_passageiros['email']=passageiro.email
            dict_passageiros['fone']=passageiro.fone
            dict_passageiros['idade']=passageiro.idade()
            if passageiro.servidor == True:
                dict_passageiros['servidor']="Sim"
            else:
                dict_passageiros['servidor']="Não"

            lista.append(dict_passageiros)
        lista_string = str(lista)
        lista_string = lista_string.replace('\'', '\"')
        #parsed_json = json.loads(lista_string)
        return lista_string

    except:
        return None