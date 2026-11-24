# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : operacoes.py
# Conteúdo : operações do menu sobre o dicionário de produtos
# ═════════════════════════════════════════════════════════════════════════════
# Todas as operações alteram apenas o dicionário (memória). O arquivo só é
# gravado quando o usuário escolhe sair (processamento em lote).
# As funções que podem alterar o inventário retornam True se alteraram,
# para o menu avisar que existem mudanças ainda não gravadas no arquivo.
#
# ID por contador: o usuário não digita o ID. Ao carregar o inventário, o
# contador começa em (maior ID existente + 1) e só aumenta, a cada camisa
# cadastrada. Assim o ID é sempre único e, durante a sessão, o ID de uma
# camisa removida não é reaproveitado.

from configuracoes import ESTOQUE_MINIMO, TAMANHOS
from validacao import ler_inteiro, ler_preco, ler_sim_nao, ler_nome, ler_texto_obrigatorio
from tela import exibir_tabela, exibir_um_produto, formatar_moeda
from busca import (existe_produto_por_id, existe_produto_por_nome,
                   busca_linear_por_nome, busca_binaria_por_nome)
from ordenacao import ordenar_por_nome


def calcular_proximo_id(produtos: dict) -> int:
    """Valor inicial do contador de IDs: maior ID cadastrado + 1."""
    maior = 0
    for id_produto in produtos:
        if id_produto > maior:
            maior = id_produto
    return maior + 1


def tamanho_da_camisa(nome: str) -> str:
    """Pela convenção do nome, o tamanho é a última palavra (ex.: 'G').
    Retorna '' se a última palavra não for um tamanho conhecido."""
    palavras = nome.split()
    if len(palavras) > 0 and palavras[-1].upper() in TAMANHOS:
        return palavras[-1].upper()
    return ''


def adicionar_produto(produtos: dict, id_produto: int) -> bool:
    """Cadastra uma camisa com o ID recebido do contador (o usuário não o digita)."""
    print('ADICIONAR CAMISA\n')
    print(f'ID gerado automaticamente: {id_produto}\n')
    print('Padrão do nome: TIME MODELO ANO TAMANHO (ex.: Real Madrid II 2026 GG)')
    print('Modelo: I = titular, II = reserva, III = terceira.')
    print(f"Tamanhos: {', '.join(TAMANHOS)}. Cada tamanho é um cadastro separado.\n")

    nome = ler_nome()
    if existe_produto_por_nome(produtos, nome):
        if not ler_sim_nao('  Já existe uma camisa com esse nome. Cadastrar mesmo assim? (S/N): '):
            print('Cadastro cancelado.')
            return False
    if tamanho_da_camisa(nome) == '':
        print('  Aviso: o nome não termina com um tamanho; ela não entrará na contagem por tamanho.')
    quantidade = ler_inteiro('Quantidade em estoque: ', minimo=0)
    preco = ler_preco('Preço unitário (R$): ')
    importado = ler_sim_nao('É importada? (S/N): ')

    produtos[id_produto] = [nome, quantidade, preco, importado]
    print(f'\nCamisa adicionada com o ID {id_produto}! (será gravada no arquivo ao sair)')
    return True


def remover_produto(produtos: dict) -> bool:
    print('REMOVER CAMISA\n')
    if len(produtos) == 0:
        print('Nenhuma camisa cadastrada.')
        return False
    id_produto = ler_inteiro('ID da camisa: ', minimo=1)
    if not existe_produto_por_id(produtos, id_produto):
        print('Nenhuma camisa com esse ID.')
        return False
    exibir_um_produto(produtos, id_produto)
    if ler_sim_nao('\nConfirma a remoção? (S/N): '):
        del produtos[id_produto]
        print('Camisa removida! (a alteração será gravada no arquivo ao sair)')
        return True
    print('Remoção cancelada.')
    return False


def atualizar_produto(produtos: dict) -> bool:
    """O ID não pode ser alterado: ele é gerado pelo contador e é a chave do dicionário."""
    print('ATUALIZAR CAMISA\n')
    if len(produtos) == 0:
        print('Nenhuma camisa cadastrada.')
        return False
    id_produto = ler_inteiro('ID da camisa: ', minimo=1)
    if not existe_produto_por_id(produtos, id_produto):
        print('Nenhuma camisa com esse ID.')
        return False

    dados = produtos[id_produto]   # é a mesma lista do dicionário: mudar aqui muda lá
    alterou = False
    while True:
        print()
        exibir_um_produto(produtos, id_produto)
        print('\n1 - Nome   2 - Quantidade   3 - Preço   4 - Importada   0 - Voltar')
        opcao = input('O que deseja alterar? ').strip()
        if opcao == '1':
            dados[0] = ler_nome('Novo nome: ')
        elif opcao == '2':
            dados[1] = ler_inteiro('Nova quantidade: ', minimo=0)
        elif opcao == '3':
            dados[2] = ler_preco('Novo preço (R$): ')
        elif opcao == '4':
            dados[3] = ler_sim_nao('É importada? (S/N): ')
        elif opcao == '0':
            return alterou
        else:
            print('Opção inválida.')
            continue
        alterou = True
        print('Alterado! (a alteração será gravada no arquivo ao sair)')


def listar_produtos(produtos: dict):
    print('CAMISAS CADASTRADAS (ordem alfabética)\n')
    if len(produtos) == 0:
        print('Nenhuma camisa cadastrada.')
        return
    lista, algoritmo = ordenar_por_nome(produtos)
    exibir_tabela(lista)
    print(f'\n{len(lista)} camisa(s). Ordenação feita com {algoritmo}.')


def buscar_produto(produtos: dict):
    print('BUSCAR CAMISA\n')
    if len(produtos) == 0:
        print('Nenhuma camisa cadastrada.')
        return
    print('1 - Por ID')
    print('2 - Por nome, busca linear  (parte do nome, ex.: flamengo ou 2026)')
    print('3 - Por nome, busca binária (nome completo, ex.: Flamengo I 2026 G)')
    opcao = input('\nOpção: ').strip()
    print()

    if opcao == '1':
        id_produto = ler_inteiro('ID: ', minimo=1)
        print()
        if existe_produto_por_id(produtos, id_produto):
            exibir_um_produto(produtos, id_produto)
        else:
            print('Nenhuma camisa com esse ID.')

    elif opcao == '2':
        termo = ler_texto_obrigatorio('Nome ou parte do nome: ')
        encontrados, comparacoes = busca_linear_por_nome(produtos, termo)
        print()
        if len(encontrados) > 0:
            exibir_tabela(encontrados)
        else:
            print('Nenhuma camisa encontrada.')
        print(f'\nBusca linear: {comparacoes} comparação(ões) no dicionário.')

    elif opcao == '3':
        nome = ler_texto_obrigatorio('Nome completo: ')
        lista, algoritmo = ordenar_por_nome(produtos)
        encontrados, comparacoes = busca_binaria_por_nome(lista, nome)
        print()
        if len(encontrados) > 0:
            exibir_tabela(encontrados)
        else:
            print('Nenhuma camisa encontrada.')
        print(f'\nLista ordenada com {algoritmo}; '
              f'busca binária: {comparacoes} comparação(ões).')

    else:
        print('Opção inválida.')


def exibir_estatisticas(produtos: dict):
    print('ESTATÍSTICAS DO ESTOQUE\n')
    if len(produtos) == 0:
        print('Nenhuma camisa cadastrada.')
        return

    total_unidades = 0
    valor_total = 0.0
    valor_importados = 0.0
    soma_precos = 0.0
    importados = 0
    sem_estoque = 0
    estoque_baixo = []
    id_mais_caro = id_mais_barato = id_maior_valor = None

    # Dicionário { tamanho: unidades em estoque }, começando tudo com zero.
    unidades_por_tamanho = {}
    for tamanho in TAMANHOS:
        unidades_por_tamanho[tamanho] = 0
    unidades_sem_tamanho = 0

    for id_produto, dados in produtos.items():
        nome, quantidade, preco, importado = dados
        valor_em_estoque = quantidade * preco
        total_unidades += quantidade
        valor_total += valor_em_estoque
        soma_precos += preco
        if importado:
            importados += 1
            valor_importados += valor_em_estoque
        if quantidade == 0:
            sem_estoque += 1
        elif quantidade <= ESTOQUE_MINIMO:
            estoque_baixo.append([id_produto] + dados)
        if id_mais_caro is None or preco > produtos[id_mais_caro][2]:
            id_mais_caro = id_produto
        if id_mais_barato is None or preco < produtos[id_mais_barato][2]:
            id_mais_barato = id_produto
        if id_maior_valor is None or valor_em_estoque > produtos[id_maior_valor][1] * produtos[id_maior_valor][2]:
            id_maior_valor = id_produto
        tamanho = tamanho_da_camisa(nome)
        if tamanho != '':
            unidades_por_tamanho[tamanho] += quantidade
        else:
            unidades_sem_tamanho += quantidade

    total_produtos = len(produtos)
    nacionais = total_produtos - importados
    mais_caro = produtos[id_mais_caro]
    mais_barato = produtos[id_mais_barato]
    maior_valor = produtos[id_maior_valor]

    partes = []
    for tamanho in TAMANHOS:
        partes.append(f'{tamanho}: {unidades_por_tamanho[tamanho]}')
    if unidades_sem_tamanho > 0:
        partes.append(f'sem tamanho: {unidades_sem_tamanho}')

    print(f'Camisas cadastradas .......: {total_produtos}')
    print(f'Unidades em estoque .......: {total_unidades}')
    print(f'Valor total do estoque ....: {formatar_moeda(valor_total)}')
    print(f'Preço médio das camisas ...: {formatar_moeda(soma_precos / total_produtos)}')
    print(f'Importadas ................: {importados} ({importados / total_produtos * 100:.1f}%)'
          f' - {formatar_moeda(valor_importados)} em estoque')
    print(f'Nacionais .................: {nacionais} ({nacionais / total_produtos * 100:.1f}%)')
    print(f'Camisa mais cara ..........: {mais_caro[0]} ({formatar_moeda(mais_caro[2])})')
    print(f'Camisa mais barata ........: {mais_barato[0]} ({formatar_moeda(mais_barato[2])})')
    print(f'Maior valor parado ........: {maior_valor[0]} '
          f'({formatar_moeda(maior_valor[1] * maior_valor[2])})')
    print(f"Unidades por tamanho ......: {' | '.join(partes)}")
    print(f'Sem estoque (quantidade 0) : {sem_estoque}')
    print(f'Estoque baixo (até {ESTOQUE_MINIMO} un.)  : {len(estoque_baixo)}')
    if len(estoque_baixo) > 0:
        print('\nCamisas com estoque baixo:')
        exibir_tabela(estoque_baixo)
