SEXO_CHOICE = (
                ('', 'Selecione uma opção'),
                ('M', 'MASCULINO'),
                ('F', 'FEMININO')
              )

DOCUMENTO_CHOICE = (
                    ('', 'Selecione uma opção'),
                    ('RG', 'RG - Registro Geral'),
                    ('CPF', 'CPF - Cadastro de Pessoa Física'),
                    ('CNH', 'CNH - Carteira Nacional de Habilitação'),
                    ('PASSAPORTE', 'Passaporte'),
                    ('RNE', 'RNE - Registro Nacional de Estrangeiros'),
                    ('TITULO', 'Título de Eleitor'),
                    ('OUTROS', 'Outros')
                )

COR_CHOICE = (
            ('', 'Selecione uma opção'),
            ('BR', 'BRANCA'),
            ('PR', 'PRETA'),
            ('AM', 'AMARELA'),
            ('PA', 'PARDA'),
            ('IN', 'INDÍGENA')
)

GRAPICH_CHOICE = (
                   (0, "--- TODOS OS GRÁFICOS ---"),
                   (1, 'STATUS (MANIFESTAÇÕES)'),
                   (2, 'SOLICITAÇÕES POR TIPO DE MANIFESTAÇÃO'),
                   (3, 'PRAZO DE ATENDIMENTO DO E-OUV'),
                   (4, 'TIPO DE IDENTIFICAÇÃO'),
                   (5, 'SOLICITAÇÕES POR OUVIDORIA')
                )

TIPO_ALTERACAO_CHOICE  = (
            ('ASSUNTO', 'Assunto'),
            ('ANALISE', 'Em análise'),
            ('TIPO_MANIFESTACAO', 'Tipo de Manifestação'),
            ('OUVIDORIA_ORIGEM', 'Movimentação de Ouvidoria'),
            ('OUVIDORIA_DESTINO', 'Movimentação de Ouvidoria'),
            ('REABRIR', 'Manifestação Reaberta'),
            ('ARQUIVAR', 'Manifestação Arquivada'),
            ('INFORMACAO_PESSOAL', 'Informação Pessoal'),
            ('PRORROGAR_PRAZO', 'Prorrogação do prazo'),
            ('ANEXO', 'Anexo'),
            ('RESPOSTA', 'Resposta intermediária'),
            ('RESPOSTA_CONCLUSIVA', 'Resposta Conclusiva'),
            ('ENCERRAR', 'Manifestação Encerrada'),
            ('COMPLEMENTAR', 'Pedido de Complementação'),
            ('RESPONSAVEL', 'Gestor Responsável')
            
)

PESQUISA_SATISFACAO_CHOICE = ((5, 'MUITO SATISFEITO'),
                             (4, 'SATISFEITO'),
                             (3, 'REGULAR'),
                             (2, 'INSATISFEITO'),
                             (1, 'MUITO INSATISFEITO'))


TIPO_MANIFESTACAO_SALA_CONTROLE_CHOICE = (('', '--- TODOS OS TIPOS ---'),
                                          ('denuncia', 'DENÚNCIA'),
                                          ('reclamacao', 'RECLAMAÇÃO'),
                                          ('solicitacao', 'SOLICITAÇÃO'),
                                          ('sugestao', 'SUGESTÃO'),
                                          ('elogio', 'ELOGIO'),
                                          ('fora-escopo', 'FORA DO ESCOPO'))

TIPO_MANIFESTACAO_CHOICE = (('denuncia', 'DENÚNCIA'),
                             ('reclamacao', 'RECLAMAÇÃO'),
                             ('solicitacao', 'SOLICITAÇÃO'),
                             ('sugestao', 'SUGESTÃO'),
                             ('elogio', 'ELOGIO'))


TIPO_MANIFESTACAO_AREA_RESTRITA_CHOICE = (('denuncia', 'DENÚNCIA'),
                             ('reclamacao', 'RECLAMAÇÃO'),
                             ('solicitacao', 'SOLICITAÇÃO'),
                             ('sugestao', 'SUGESTÃO'),
                             ('elogio', 'ELOGIO'),
                             ('fora-escopo', 'FORA DO ESCOPO'))

FERIADO_TIPO  = (('M', 'MUNICIPAL'),
                 ('E', 'ESTADUAL'),
                 ('F', 'FEDERAL'))

IDENTIFICACAO_CHOICES = (
                    ('T', 'Todos'),
                    ('I', 'O cidadão se identificou'),
                    ('A', 'O cidadão não se identificou'))
    
GESTOR_STATUS = (
                ('T', 'TODOS'),
                ('A', 'ATIVO'),
                ('I', 'INATIVO'))

TIPO_ENTRADA_MANIFESTACAO = (
                ('T', 'TODOS'),
                ('E', 'SISTEMA E-OUV'),
                ('P', 'PRESENCIAL'))