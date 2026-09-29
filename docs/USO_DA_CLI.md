# Guia de uso da CLI

Execute a partir da pasta `SuperTranslet_Mestre` com Python 3.10+.

## Menu mestre

```bash
python -m NovosSistemas
```

O menu permite: **1)** aprender arquivos, **2)** abrir chat, **3)** fazer pergunta, **4)** visualizar ParteA/ParteB e **5)** sair.

## Escolher arquivo por lista numérica

```bash
python -m NovosSistemas.cli --modo aprender --diretorio /caminho/dos/documentos
```

A CLI lista extensões suportadas e aceita `1`, `1,3` ou `todos`. A pasta é percorrida recursivamente, a menos que se use `--sem-recursao`.

```bash
python -m NovosSistemas.cli --modo aprender --diretorio ./docs --selecionar 2
python -m NovosSistemas.cli --modo aprender --diretorio ./docs --selecionar 1,4
python -m NovosSistemas.cli --modo aprender --diretorio ./docs --selecionar todos
```

## Escolher por caminho

```bash
python -m NovosSistemas.cli --modo aprender --arquivo ./guia.pdf
python -m NovosSistemas.cli --modo aprender --arquivo ./guia.pdf ./notas.txt
```

## Interação, chatbot e resposta pontual

```bash
# Perguntas sucessivas diretamente sobre a base aprendida
python -m NovosSistemas.cli --modo interacao

# Interface de conversa em subpasta própria
python -m NovosSistemas.cli --modo chatbot
python -m NovosSistemas.cli --modo responder --pergunta "Como o material define ParteA?"
```

A consulta retorna a fonte. O chatbot termina com `/sair`, `sair`, `tchau` ou `fim`.

## Opções comuns

- `--modelo CAMINHO`: JSON da base de aprendizado. Padrão `NovosSistemas/dados/base_aprendizado.json`.
- `--modo menu|aprender|interacao|chatbot|responder|mapa`: escolhe sistema e modo sem entrar no menu mestre.
- `--diretorio PASTA`: pasta a pesquisar durante aprendizado.
- `--arquivo CAMINHO [CAMINHO ...]`: um ou mais arquivos exatos.
- `--selecionar N[,N...]|todos`: escolhe por posição na lista. Exemplo: `2,5`.
- `--sem-recursao`: não entra em subpastas.
- `--pergunta TEXTO`: texto para o modo `responder`.

Ver ajuda da ferramenta:

```bash
python -m NovosSistemas.cli --help
```

O algoritmo é local: a operação **aprender** grava uma base JSON; **chatbot** e **responder** consultam essa base. Use `--modelo` igual nos modos para compartilhar o mesmo aprendizado.
