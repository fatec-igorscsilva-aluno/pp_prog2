# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : configuracoes.py
# Conteúdo : constantes usadas por todos os outros módulos
# ═════════════════════════════════════════════════════════════════════════════

import os

NOME_SISTEMA = 'INVENTÁRIO DE CAMISAS DE FUTEBOL'

# Os arquivos ficam na pasta do programa, não importa de onde ele foi executado.
PASTA_PROGRAMA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_LOGIN = os.path.join(PASTA_PROGRAMA, 'login.txt')
ARQUIVO_INVENTARIO = os.path.join(PASTA_PROGRAMA, 'inventario.csv')

SEPARADOR = ';'
LIMITE_ORDENACAO_SIMPLES = 100   # até 100 camisas: Insertion Sort; acima: Merge Sort
ESTOQUE_MINIMO = 5               # até isso a camisa aparece como "estoque baixo"
TAMANHO_MAXIMO_NOME = 34
TAMANHO_MINIMO_SENHA = 6
TENTATIVAS_ANTES_DA_ESPERA = 3

# Tamanhos reconhecidos no final do nome (usados nas estatísticas).
TAMANHOS = ['PP', 'P', 'M', 'G', 'GG', 'XG']

# Cifra de César: cada caractere é trocado pelo que está CHAVE_CESAR
# posições à frente neste alfabeto (dando a volta no final).
# O alfabeto tem 103 símbolos e NÃO contém ';', assim o texto cifrado
# nunca "quebra" o separador do CSV. Inclui ü, ñ e apóstrofo por causa
# de nomes como Bayern München, Peñarol e Newell's.
ALFABETO = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            'abcdefghijklmnopqrstuvwxyz'
            '0123456789'
            'ÁÀÂÃÉÊÍÓÔÕÚÇáàâãéêíóôõúçüñ'
            " .,-_/()+&%!?:'")
CHAVE_CESAR = 7
