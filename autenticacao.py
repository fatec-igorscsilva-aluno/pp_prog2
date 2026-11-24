# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : autenticacao.py
# Conteúdo : hash SHA-256 e login (arquivo login.txt)
# ═════════════════════════════════════════════════════════════════════════════
# Escolha: SHA-256 (módulo hashlib). Hash é uma função de mão única: dá
# para calcular o hash a partir da senha, mas não a senha a partir do hash.
# Por isso o login funciona comparando HASH com HASH, e o arquivo nunca
# guarda o usuário nem a senha em texto claro.
# Limitação: sem "sal" (salt), senhas iguais geram hashes iguais e senhas
# fracas podem ser achadas em tabelas prontas (rainbow tables).
#
# login.txt -> linha 1: hash do usuário / linha 2: hash da senha

import os
import hashlib   # função de hash SHA-256
import getpass   # lê a senha sem mostrar o que é digitado
import time      # espera após várias tentativas de login erradas
from configuracoes import ARQUIVO_LOGIN, TAMANHO_MINIMO_SENHA, TENTATIVAS_ANTES_DA_ESPERA
from validacao import ler_texto_obrigatorio


def gerar_hash(texto: str) -> str:
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


def ler_login():
    """Retorna (hash_usuario, hash_senha), ou None se login.txt estiver vazio/incompleto."""
    linhas = []
    with open(ARQUIVO_LOGIN, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha != '':
                linhas.append(linha)
    if len(linhas) < 2:
        return None
    return linhas[0], linhas[1]


def salvar_login(usuario: str, senha: str):
    """Sobrescreve login.txt com os hashes do usuário e da senha."""
    with open(ARQUIVO_LOGIN, 'w', encoding='utf-8') as arquivo:
        arquivo.write(gerar_hash(usuario) + '\n')
        arquivo.write(gerar_hash(senha) + '\n')


def cadastrar_credenciais():
    """Pede usuário e senha novos (senha com confirmação) e grava em login.txt."""
    usuario = ler_texto_obrigatorio('Novo usuário: ')
    while True:
        senha = getpass.getpass(f'Nova senha (mínimo {TAMANHO_MINIMO_SENHA} caracteres): ')
        if len(senha) < TAMANHO_MINIMO_SENHA:
            print(f'  A senha precisa ter pelo menos {TAMANHO_MINIMO_SENHA} caracteres.')
            continue
        confirmacao = getpass.getpass('Confirme a nova senha: ')
        if senha != confirmacao:
            print('  As senhas não conferem. Tente novamente.')
            continue
        break
    salvar_login(usuario, senha)


def preparar_login() -> bool:
    """Garante que login.txt exista e tenha credenciais.
    Retorna True se for o primeiro acesso ao sistema."""
    if not os.path.exists(ARQUIVO_LOGIN):
        open(ARQUIVO_LOGIN, 'w', encoding='utf-8').close()
        print('Arquivo login.txt não encontrado: um arquivo novo foi criado.')
    if ler_login() is None:
        print('\nPRIMEIRO ACESSO: cadastre o usuário e a senha iniciais.\n')
        cadastrar_credenciais()
        print('\nUsuário cadastrado! Agora faça o login.\n')
        return True
    return False


def fazer_login():
    """Repete até o usuário acertar. O usuário e a senha digitados passam
    pelo hash e são comparados com os hashes guardados em login.txt."""
    hash_usuario, hash_senha = ler_login()
    tentativas = 0
    while True:
        usuario = input('Usuário: ').strip()
        senha = getpass.getpass('Senha: ')
        if gerar_hash(usuario) == hash_usuario and gerar_hash(senha) == hash_senha:
            print('\nAcesso permitido!')
            return
        tentativas += 1
        # A mensagem não diz se o erro foi no usuário ou na senha,
        # para não ajudar quem está tentando adivinhar.
        print('Usuário ou senha incorretos. Acesso negado.\n')
        if tentativas >= TENTATIVAS_ANTES_DA_ESPERA:
            # Cada erro a mais aumenta a espera: atrasa ataques de força bruta.
            print(f'Muitas tentativas. Aguarde {tentativas} segundos...\n')
            time.sleep(tentativas)


def alterar_credenciais():
    """Opção do menu para sobrescrever usuário e senha do login.txt.
    Pede a senha atual antes, para que ninguém troque o login de quem
    deixou o computador aberto."""
    print('ALTERAR USUÁRIO E SENHA\n')
    hash_senha = ler_login()[1]
    senha_atual = getpass.getpass('Confirme a senha ATUAL: ')
    if gerar_hash(senha_atual) != hash_senha:
        print('Senha incorreta. Operação cancelada.')
        return
    cadastrar_credenciais()
    print('\nUsuário e senha alterados com sucesso!')
