# ═════════════════════════════════════════════════════════════════════════════
# Projeto  : Inventário de Camisas de Futebol
# Módulo   : criptografia.py
# Conteúdo : Cifra de César usada no arquivo inventario.csv
# ═════════════════════════════════════════════════════════════════════════════
# Escolha: cifra de substituição com deslocamento fixo, implementada pela
# equipe. Usamos um alfabeto próprio, maior que o tradicional (só A-Z),
# para cifrar também números, acentos e o valor True/False.
# Limitação: com 103 símbolos só existem 102 chaves possíveis, então um
# ataque de força bruta testa todas em milésimos de segundo. Serve para
# fins didáticos, não para proteger dados reais.

from configuracoes import ALFABETO, CHAVE_CESAR


def cifrar(texto: str, chave: int = CHAVE_CESAR) -> str:
    """Retorna o texto com cada caractere deslocado 'chave' posições no ALFABETO."""
    resultado = ''
    for caractere in texto:
        if caractere in ALFABETO:
            posicao = ALFABETO.index(caractere)
            nova_posicao = (posicao + chave) % len(ALFABETO)
            resultado += ALFABETO[nova_posicao]
        else:
            resultado += caractere   # fora do alfabeto: fica igual
    return resultado


def decifrar(texto: str, chave: int = CHAVE_CESAR) -> str:
    """Desfaz a cifra deslocando para trás (chave negativa)."""
    return cifrar(texto, -chave)


def main():
    # Teste rápido do módulo: python3 criptografia.py
    texto = input('Texto para cifrar: ')
    cifrado = cifrar(texto)
    print(f'Cifrado  : {cifrado}')
    print(f'Decifrado: {decifrar(cifrado)}')


if __name__ == '__main__':
    main()
