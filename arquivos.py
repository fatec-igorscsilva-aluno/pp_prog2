# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : arquivos.py
# Conteúdo : leitura e gravação do inventario.csv (processamento em lote)
# ═════════════════════════════════════════════════════════════════════════════
# O arquivo é lido uma vez, logo após o login, e gravado uma vez, ao sair.
# Entre esses dois momentos, tudo acontece no dicionário (memória RAM).
# Vantagem: poucas operações de disco e o arquivo só muda ao final.
# Desvantagem: se o programa for fechado à força ou faltar energia,
# as alterações da sessão se perdem. Além disso, na RAM os dados
# ficam decifrados (desprotegidos).
#
# inventario.csv -> uma camisa por linha: id;nome;quantidade;preco;importado
#                   com cada campo cifrado separadamente (Cifra de César)

import os
from configuracoes import ARQUIVO_INVENTARIO, PASTA_PROGRAMA, SEPARADOR
from criptografia import cifrar, decifrar
from validacao import ler_sim_nao


def carregar_inventario() -> dict:
    """Lê inventario.csv, decifra cada campo e monta o dicionário de produtos."""
    produtos = {}
    with open(ARQUIVO_INVENTARIO, 'r', encoding='utf-8') as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.rstrip('\n')   # não usar strip(): espaço faz parte da cifra
            if linha.strip() == '':
                continue
            campos = linha.split(SEPARADOR)
            if len(campos) != 5:
                print(f'Aviso: linha {numero_linha} ignorada (formato inválido).')
                continue
            try:
                id_produto = int(decifrar(campos[0]))
                nome = decifrar(campos[1])
                quantidade = int(decifrar(campos[2]))
                preco = float(decifrar(campos[3]))
                importado = decifrar(campos[4]) == 'True'
            except ValueError:
                print(f'Aviso: linha {numero_linha} ignorada (dados corrompidos ou chave errada).')
                continue
            if id_produto in produtos:
                print(f'Aviso: linha {numero_linha} ignorada (ID {id_produto} repetido).')
                continue
            produtos[id_produto] = [nome, quantidade, preco, importado]
    return produtos


def salvar_inventario(produtos: dict):
    """Cifra cada campo de cada produto e grava tudo em inventario.csv."""
    with open(ARQUIVO_INVENTARIO, 'w', encoding='utf-8') as arquivo:
        for id_produto, dados in produtos.items():
            nome, quantidade, preco, importado = dados
            campos = [str(id_produto), nome, str(quantidade), str(preco), str(importado)]
            campos_cifrados = []
            for campo in campos:
                campos_cifrados.append(cifrar(campo))
            arquivo.write(SEPARADOR.join(campos_cifrados) + '\n')


def preparar_inventario(primeiro_acesso: bool):
    """Carrega o inventário. Retorna o dicionário, ou None se o usuário
    preferir encerrar para colocar o arquivo no lugar certo."""
    if os.path.exists(ARQUIVO_INVENTARIO):
        produtos = carregar_inventario()
        print(f'Inventário decifrado e carregado: {len(produtos)} camisa(s).')
        return produtos

    if primeiro_acesso:
        salvar_inventario({})
        print('Um arquivo inventario.csv vazio foi criado.')
        return {}

    print('\nATENÇÃO: o arquivo inventario.csv não foi encontrado em:')
    print(f'  {PASTA_PROGRAMA}')
    if ler_sim_nao('Deseja criar um inventário novo e vazio? (S/N): '):
        salvar_inventario({})
        print('Um arquivo inventario.csv vazio foi criado.')
        return {}
    print('\nColoque o arquivo inventario.csv na pasta acima e execute o programa novamente.')
    return None
