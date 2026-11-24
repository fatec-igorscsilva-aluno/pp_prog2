# Inventário de Camisas de Futebol

Este é o Projeto de Programação de Programação II (Prof. Lucio), com o tema **loja de camisas de futebol**. 

## Arquivos do projeto

O código segue a organização das aulas, com um arquivo por assunto:

| Arquivo | Conteúdo |
|---|---|
| `main.py` | programa principal e menu (é este que se executa) |
| `configuracoes.py` | constantes: nomes dos arquivos, alfabeto e chave da cifra, limites |
| `autenticacao.py` | hash SHA-256, login e troca de usuário e senha (`login.txt`) |
| `criptografia.py` | Cifra de César |
| `arquivos.py` | leitura e gravação do `inventario.csv` (processamento em lote) |
| `operacoes.py` | adicionar, remover, atualizar, listar, buscar, estatísticas e contador de ID |
| `busca.py` | busca linear e busca binária |
| `ordenacao.py` | Insertion Sort, Merge Sort e escolha automática |
| `validacao.py` | leitura do teclado com validação |
| `tela.py` | tabela, formato da moeda, cabeçalho e limpeza da tela |

Uma divisão possível para a apresentação: (1) `main.py` e `arquivos.py`, com o processamento em lote, (2) `operacoes.py`, com o dicionário e o contador, (3) `busca.py` e `ordenacao.py`, (4) `autenticacao.py`, (5) `criptografia.py` e `validacao.py`.

## ID automático

O usuário **não digita o ID**. Ao carregar o inventário, o contador começa no maior ID existente + 1 e avança a cada camisa cadastrada (`calcular_proximo_id` em `operacoes.py` e `proximo_id` em `main.py`). Durante a sessão, o ID de uma camisa removida não é reaproveitado, e um cadastro cancelado não faz o contador avançar. Nas opções de remover, atualizar e buscar, o usuário digita o ID da camisa que quer escolher.

## Como cadastrar as camisas

O PDF define os campos (ID, nome, quantidade, preço, importado). Por isso, o time, o modelo, o ano e o tamanho vão juntos no **nome**, sempre nesta ordem:

```
TIME MODELO ANO TAMANHO        ex.: Flamengo I 2026 G
                                    Real Madrid II 2026 GG
```

- **Modelo:** I = titular, II = reserva, III = terceira.
- **Tamanhos:** PP, P, M, G, GG, XG. Cada tamanho é um cadastro separado, porque cada um tem o seu estoque.
- **Importada:** "S" para camisas de times de fora (Real Madrid, PSG...), "N" para as nacionais.

