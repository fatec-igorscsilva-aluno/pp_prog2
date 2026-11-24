# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : tela.py
# Conteúdo : funções de exibição no terminal
# ═════════════════════════════════════════════════════════════════════════════

import os
from configuracoes import NOME_SISTEMA


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input('\nPressione ENTER para continuar...')


def cabecalho():
    print('=' * 78)
    print(NOME_SISTEMA.center(78))
    print('=' * 78)


def formatar_moeda(valor: float) -> str:
    """1234.5 -> 'R$ 1.234,50' (padrão brasileiro)."""
    texto = f'{valor:,.2f}'                       # '1,234.50'
    texto = texto.replace(',', '#').replace('.', ',').replace('#', '.')
    return 'R$ ' + texto


def exibir_tabela(lista_produtos: list):
    """Mostra uma lista no formato [[id, nome, quantidade, preco, importado], ...]."""
    print(f"{'ID':>5} | {'CAMISA':<34} | {'QTD':>5} | {'PREÇO':>13} | IMPORTADA")
    print('-' * 78)
    for id_produto, nome, quantidade, preco, importado in lista_produtos:
        texto_importado = 'Sim' if importado else 'Não'
        print(f'{id_produto:>5} | {nome:<34} | {quantidade:>5} | '
              f'{formatar_moeda(preco):>13} | {texto_importado:^9}')


def exibir_um_produto(produtos: dict, id_produto: int):
    exibir_tabela([[id_produto] + produtos[id_produto]])
