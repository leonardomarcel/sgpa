# -*- coding: utf-8 -*-
from util.util import get_gestor_by_id
u"""."""


def get_list(user=None):
    u"""Lista para criação do menu.

    menulist = [<nivel do menu>, <label do menu>, <url>, <img css>,
        <flag p/ mostrar menu>]
        <nivel do menu> = 1, 2, 3
        <img css> = icones contidos no font-awesome,
        http://fortawesome.github.io/Font-Awesome/icons/
    """
    menulist = list()

    menulist.append([1, 'Início', '/passagem/index', 'fas fa-home', True])
    menulist.append([1, 'Usuários', '/auth_local/usuarios', 'fas fa-users', True])
    menulist.append([1, 'Passageiros', '/passagem/passageiros', 'fas fa-users', True])
    menulist.append([1, 'Passagens', '/', 'fas fa-laptop-medical', True])
    menulist.append([2, 'Aeroportos', '/passagem/aeroportos', 'fas fa-book', True])
    menulist.append([2, 'Agências de Viagem', '/passagem/agencias_viagem', 'fas fa-book', True])
    menulist.append([2, 'Cotas', '/passagem/cotas', 'fas fa-laptop-medical', True])
    menulist.append([2, 'Companhias Aéreas', '/passagem/companhias_aereas', 'fas fa-laptop-medical', True])
    menulist.append([2, 'Rotas', '/passagem/rotas', 'fas fa-laptop-medical', True])
    menulist.append([2, 'Solicitações Passagem', '/passagem/solicitacoes_passagem', 'fas fa-book', True])
    menulist.append([1, 'Relatórios', '/', 'fas fa-laptop-medical', True])
    menulist.append([2, 'Relatório Analítico Passagem Período', '/relatorio/form_passagem_periodo', 'fas fa-book', True])
    menulist.append([2, 'Relatório Contábil Passagem Período', '/relatorio/form_passagem_periodo_contabil', 'fas fa-book', True])
    
    
    
    return menulist

