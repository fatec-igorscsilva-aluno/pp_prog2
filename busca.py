# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : busca.py
# Conteúdo : verificação de existência, busca linear e busca binária
# ═════════════════════════════════════════════════════════════════════════════
# Busca por ID: acesso direto ao dicionário (a chave É o ID), sem percorrer nada.
# Busca linear por nome: percorre o dicionário item a item, O(n). Aceita
#   parte do nome ("flamengo" acha todas as camisas do Flamengo, "2026"
#   acha todas as da temporada), porque olha todos os itens.
# Busca binária por nome: precisa de uma lista ORDENADA; a cada comparação
#   descarta metade da lista, O(log n). Só acha o nome completo
#   ("Flamengo I 2026 G"), já que depende da ordem alfabética. Observação:
#   ordenar custa mais do que uma busca linear, então a binária compensa
#   quando se ordena uma vez e se busca várias vezes na mesma lista.

from ordenacao import chave_nome


def existe_produto_por_id(produtos: dict, id_produto: int) -> bool:
    return id_produto in produtos


def existe_produto_por_nome(produtos: dict, nome: str) -> bool:
    nome = nome.lower()
    for dados in produtos.values():
        if dados[0].lower() == nome:
            return True
    return False


def busca_linear_por_nome(produtos: dict, termo: str):
    """Retorna (produtos cujo nome contém o termo, número de comparações)."""
    termo = termo.lower()
    encontrados = []
    comparacoes = 0
    for id_produto, dados in produtos.items():
        comparacoes += 1
        if termo in dados[0].lower():
            encontrados.append([id_produto] + dados)
    return encontrados, comparacoes


def busca_binaria_por_nome(lista_ordenada: list, nome: str):
    """Retorna (produtos com exatamente esse nome, número de comparações)."""
    nome = nome.lower()
    inicio = 0
    fim = len(lista_ordenada) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        nome_meio = chave_nome(lista_ordenada[meio])
        comparacoes += 1
        if nome_meio == nome:
            # Achou um. Como a lista está ordenada, produtos com o mesmo
            # nome estão encostados nele: andamos para os lados para pegá-los.
            primeiro = meio
            while primeiro > 0 and chave_nome(lista_ordenada[primeiro - 1]) == nome:
                primeiro -= 1
            ultimo = meio
            while ultimo < len(lista_ordenada) - 1 and chave_nome(lista_ordenada[ultimo + 1]) == nome:
                ultimo += 1
            return lista_ordenada[primeiro:ultimo + 1], comparacoes
        if nome_meio < nome:
            inicio = meio + 1   # o nome procurado só pode estar na metade direita
        else:
            fim = meio - 1      # ... ou na metade esquerda
    return [], comparacoes
