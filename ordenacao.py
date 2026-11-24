# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : ordenacao.py
# Conteúdo : Insertion Sort, Merge Sort e escolha automática do algoritmo
# ═════════════════════════════════════════════════════════════════════════════
# Para ordenar, o dicionário vira uma lista de produtos:
#     [[id, nome, quantidade, preco, importado], ...]
# e a comparação é feita pelo nome em minúsculas ("flamengo" e "Flamengo" empatam).
# Como o nome começa pelo time, a listagem fica agrupada por time.
#
# Insertion Sort (até 100 camisas): O(n²) no pior caso, mas simples, não
#   usa memória extra e é rápido para listas pequenas ou quase ordenadas.
# Merge Sort (mais de 100 camisas): O(n log n) sempre, mas usa uma lista
#   auxiliar. Para listas grandes a diferença compensa: com 10.000 itens são
#   ~50 milhões de comparações no Insertion contra ~130 mil no Merge.
#
# As funções seguem o modelo das aulas (insere/insertion_sort e
# mescla/merge_sort), trocando a comparação de números pela de nomes.

from configuracoes import LIMITE_ORDENACAO_SIMPLES


def chave_nome(produto: list) -> str:
    """Valor usado para comparar dois produtos na ordenação e na busca."""
    return produto[1].lower()


def insere(x: list, L: list, n: int):
    """Insere x na parte já ordenada L[0..n-1], empurrando os maiores para a direita."""
    u = n - 1
    while u >= 0 and chave_nome(x) < chave_nome(L[u]):
        L[u + 1] = L[u]
        u -= 1
    L[u + 1] = x


def insertion_sort(L: list):
    i = 1
    while i < len(L):
        insere(L[i], L, i)
        i += 1


def mescla(L: list, i: int, m: int, f: int):
    """Junta as metades ordenadas L[i..m] e L[m+1..f] numa lista temporária T."""
    h, j, k = i, m + 1, 0
    T = [None] * (f - i + 1)
    while h <= m and j <= f:
        if chave_nome(L[h]) <= chave_nome(L[j]):
            T[k] = L[h]
            h += 1
        else:
            T[k] = L[j]
            j += 1
        k += 1
    while h <= m:
        T[k] = L[h]
        h += 1
        k += 1
    while j <= f:
        T[k] = L[j]
        j += 1
        k += 1
    for z in range(len(T)):
        L[i + z] = T[z]


def merge_sort(L: list, i: int, f: int):
    """Divide a lista ao meio, ordena cada metade (recursão) e mescla."""
    if i >= f:
        return
    m = (i + f) // 2
    merge_sort(L, i, m)
    merge_sort(L, m + 1, f)
    mescla(L, i, m, f)


def dicionario_para_lista(produtos: dict) -> list:
    lista = []
    for id_produto, dados in produtos.items():
        lista.append([id_produto, dados[0], dados[1], dados[2], dados[3]])
    return lista


def ordenar_por_nome(produtos: dict):
    """Retorna (lista ordenada por nome, nome do algoritmo usado).
    O sistema escolhe o algoritmo sozinho, pela quantidade de produtos."""
    lista = dicionario_para_lista(produtos)
    if len(lista) <= LIMITE_ORDENACAO_SIMPLES:
        insertion_sort(lista)
        return lista, 'Insertion Sort'
    merge_sort(lista, 0, len(lista) - 1)
    return lista, 'Merge Sort'
