# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : validacao.py
# Conteúdo : leitura do teclado com validação das entradas
# ═════════════════════════════════════════════════════════════════════════════
# Toda leitura do teclado repete a pergunta até receber um valor válido,
# assim um dado errado nunca chega ao dicionário (nem ao arquivo) e o
# programa não fecha com erro ao receber, por exemplo, letras no lugar
# de um número.

import math      # math.isfinite: rejeita valores como 'nan' e 'inf'
from configuracoes import ALFABETO, TAMANHO_MAXIMO_NOME


def ler_texto_obrigatorio(mensagem: str) -> str:
    while True:
        texto = input(mensagem).strip()
        if texto != '':
            return texto
        print('  Este campo não pode ficar vazio.')


def ler_inteiro(mensagem: str, minimo: int = None) -> int:
    while True:
        texto = input(mensagem).strip()
        try:
            numero = int(texto)
        except ValueError:
            print('  Valor inválido: digite um número inteiro.')
            continue
        if minimo is not None and numero < minimo:
            print(f'  O valor precisa ser maior ou igual a {minimo}.')
            continue
        return numero


def ler_preco(mensagem: str) -> float:
    while True:
        texto = input(mensagem).strip().replace(',', '.')   # aceita 349,90 ou 349.90
        try:
            preco = float(texto)
        except ValueError:
            print('  Valor inválido: use um número como 349.90 ou 349,90.')
            continue
        if not math.isfinite(preco) or preco < 0:
            print('  O preço precisa ser um número maior ou igual a zero.')
            continue
        return round(preco, 2)


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().upper()
        if resposta in ('S', 'SIM'):
            return True
        if resposta in ('N', 'NAO', 'NÃO'):
            return False
        print('  Responda com S ou N.')


def ler_nome(mensagem: str = 'Nome (ex.: Flamengo I 2026 G): ') -> str:
    """O nome só pode ter caracteres do ALFABETO da cifra. Assim todo o nome
    fica cifrado no arquivo e um ';' digitado não quebra o CSV."""
    while True:
        nome = ler_texto_obrigatorio(mensagem)
        if len(nome) > TAMANHO_MAXIMO_NOME:
            print(f'  O nome pode ter no máximo {TAMANHO_MAXIMO_NOME} caracteres.')
            continue
        invalidos = ''
        for caractere in nome:
            if caractere not in ALFABETO and caractere not in invalidos:
                invalidos += caractere
        if invalidos != '':
            print(f'  Caracteres não permitidos: {invalidos}')
            print("  Use letras, números, espaço e . , - _ / ( ) + & % ! ? : '")
            continue
        return nome
