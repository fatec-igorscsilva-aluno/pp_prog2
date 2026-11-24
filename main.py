# ═════════════════════════════════════════════════════════════════════════════
# Projeto    : Sistema de Gestão de Inventário com Segurança da Informação
# Tema       : Loja de camisas de futebol
# Disciplina : Programação II - Prof. Lucio Nunes de Lira
# Curso      : Segurança da Informação 
# Equipe     : COUPGUYS
# ═════════════════════════════════════════════════════════════════════════════
# Módulos do projeto:
#     main.py           -> programa principal e menu (este arquivo)
#     configuracoes.py  -> constantes (nomes dos arquivos, alfabeto, chave...)
#     autenticacao.py   -> hash SHA-256 e login (login.txt)
#     criptografia.py   -> Cifra de César
#     arquivos.py       -> leitura e gravação do inventario.csv
#     operacoes.py      -> adicionar, remover, atualizar, listar, buscar, estatísticas
#     busca.py          -> busca linear e busca binária
#     ordenacao.py      -> Insertion Sort e Merge Sort
#     validacao.py      -> leitura do teclado com validação
#     tela.py           -> tabela, moeda, cabeçalho, limpar a tela
#
# Estrutura do inventário na memória (dicionário = tabela):
#     produtos = { ID: [nome, quantidade, preco, importado], ... }
#     ex.:       { 7: ['Flamengo I 2026 G', 15, 349.9, False] }
#
# Padrão do nome de cada camisa: TIME MODELO ANO TAMANHO
#     ex.: 'Flamengo I 2026 G', 'Real Madrid II 2026 GG'
#     (I = titular, II = reserva, III = terceira camisa)
#
# ═════════════════════════════════════════════════════════════════════════════

from tela import limpar_tela, pausar, cabecalho
from autenticacao import preparar_login, fazer_login, alterar_credenciais
from arquivos import preparar_inventario, salvar_inventario
from operacoes import (calcular_proximo_id, adicionar_produto, remover_produto,
                       atualizar_produto, listar_produtos, buscar_produto,
                       exibir_estatisticas)


def menu_principal(produtos: dict):
    proximo_id = calcular_proximo_id(produtos)   # contador de IDs
    alteracoes_pendentes = False
    while True:
        limpar_tela()
        cabecalho()
        print(f'Camisas cadastradas: {len(produtos)}')
        if alteracoes_pendentes:
            print('(*) Há alterações que só serão gravadas no arquivo ao sair.')
        print()
        print('1 - Adicionar camisa')
        print('2 - Remover camisa')
        print('3 - Atualizar camisa')
        print('4 - Listar camisas (ordem alfabética)')
        print('5 - Buscar camisa')
        print('6 - Estatísticas do estoque')
        print('7 - Alterar usuário e senha')
        print('0 - Salvar e sair')
        opcao = input('\nEscolha uma opção: ').strip()
        limpar_tela()
        cabecalho()
        print()

        if opcao == '1':
            if adicionar_produto(produtos, proximo_id):
                proximo_id += 1   # o contador só avança se a camisa foi cadastrada
                alteracoes_pendentes = True
        elif opcao == '2':
            if remover_produto(produtos):
                alteracoes_pendentes = True
        elif opcao == '3':
            if atualizar_produto(produtos):
                alteracoes_pendentes = True
        elif opcao == '4':
            listar_produtos(produtos)
        elif opcao == '5':
            buscar_produto(produtos)
        elif opcao == '6':
            exibir_estatisticas(produtos)
        elif opcao == '7':
            alterar_credenciais()
        elif opcao == '0':
            salvar_inventario(produtos)
            print('Inventário cifrado e gravado em inventario.csv. Até logo!')
            return
        else:
            print('Opção inválida.')
        pausar()


def main():
    limpar_tela()
    cabecalho()
    print()
    primeiro_acesso = preparar_login()
    fazer_login()
    produtos = preparar_inventario(primeiro_acesso)
    if produtos is None:
        return
    pausar()
    menu_principal(produtos)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\n\nPrograma interrompido. Alterações não salvas foram perdidas.')
