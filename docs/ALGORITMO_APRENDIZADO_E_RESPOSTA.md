# Especificação completa — aprendizado e resposta SuperTranslet

## 1. Objetivo e limite do algoritmo

`NovosSistemas/aprendizado/modelo.py` implementa um sistema de **aprendizado documental local por recuperação de informação**. O material de treino são arquivos escolhidos pela pessoa usuária. O programa converte-os em texto, divide o texto em trechos, registra cada trecho com o caminho da fonte e ordena os trechos que melhor correspondem a uma pergunta.

Não é uma rede neural, não faz fine-tuning, não envia arquivos para a nuvem e não inventa uma resposta generativa. A resposta é um excerto efetivamente encontrado na base, acompanhado do caminho de origem. A pontuação serve para ordenar candidatos, não é probabilidade calibrada de verdade.

## 2. Ideia ParteA e ParteB

O protótipo original contém uma sequência de símbolos (`fletra_A`/ParteA) e outra de números (`fletra_B`/ParteB). A ideia preservada é que cada posição `i` de ParteA tenha um código numérico na posição `i` de ParteB:

```text
ParteA[i] ↔ ParteB[i]
```

A implementação nova torna a regra explícita, única e validada. Os códigos são **categorias de caractere**, e não significados de palavras:

| ParteB | Grupo de caracteres (ParteA) | Exemplos |
|---:|---|---|
| 1 | Letras maiúsculas | `A-Z` |
| 2 | Letras minúsculas | `a-z` |
| 3 | Algarismos | `0-9` |
| 4 | Operadores | `+ - * / ^ % =` |
| 5 | Pontuação | `. , ? ! ; :` |
| 6 | Espaços em branco | espaço, tabulação, nova linha, retorno de carro |
| 7 | Delimitadores e outros sinais | `_ [ ] { } ( ) < > \\ \| @ # $ & ~ ` aspas |
| 0 | Caractere não mapeado | por exemplo, emoji |

`PARTE_A` e `PARTE_B` são tuplas alinhadas geradas dos grupos; o programa verifica que têm o mesmo comprimento e que ParteA não contém duplicatas. `MAPA_CARACTERE_NUMERO` é o dicionário resultante. Acentos e alfabetos Unicode são tratados por regra: letra maiúscula → 1; minúscula → 2; caractere numérico → 3; espaço Unicode → 6. Símbolos Unicode desconhecidos → 0. O arquivo legível `NovosSistemas/aprendizado/mapeamento_parte_a_parte_b.json` documenta esses grupos.

**Compatibilidade:** a tabela não afirma reproduzir literalmente todos os números experimentais do código antigo. Em `SuperBrain/.../Zsx.py` e `Linz.py`, as strings de símbolos/números variam e nem sempre têm o mesmo comprimento; a função antiga também agrega categorias por comparações de caractere. A extensão nova corrige o alinhamento apenas dentro de seu próprio namespace e deixa as rotinas antigas intactas.

## 3. Fluxo de aprendizado

### Etapa 1 — seleção

A CLI aceita caminhos explícitos, uma pasta para varredura ou índices numéricos da lista. A numeração começa em 1. Selecionar `1,3` escolhe dois itens; `todos` inclui cada formato suportado na pasta. Por padrão, a busca em pasta é recursiva.

### Etapa 2 — extração do conteúdo

`leitores.ler_documento()` escolhe o extrator pela extensão. Ele lê texto, tabelas, XML ou conteúdo de pacotes abertos; recusa arquivo inexistente, extensão desconhecida e arquivos sem texto extraível. Não executa macros. PDF digitalizado (imagem sem camada textual) precisa de OCR, que não está incluído.

### Etapa 3 — preparação e segmentação

1. Normaliza quebras de linha.
2. Separa parágrafos por linhas vazias.
3. Separa frases em pontuação terminal (`.`, `!`, `?`) quando há espaço subsequente.
4. Junta frases até um limite aproximado de 1.200 caracteres; frases excessivamente longas são repartidas por palavras.
5. Descarta trechos vazios.

A divisão é deliberadamente local e simples; siglas, pontuação multilíngue e layout complexo podem não segmentar perfeitamente.

### Etapa 4 — identidade e deduplicação

Para cada documento e trecho calcula-se SHA-256 de `caminho + NUL + conteúdo normalizado`. Assim, reaprender o mesmo conteúdo do mesmo caminho não duplica trechos. Cópias idênticas sob caminhos distintos são mantidas, pois a proveniência é diferente.

### Etapa 5 — representação e índice

Na consulta, as palavras Unicode são extraídas por expressão regular e normalizadas com Unicode NFKC + `casefold()`; os acentos são preservados. Para comparação por categorias, cada caractere recebe seu código ParteB. A base persistente guarda conteúdo, IDs, caminhos e metadados; estatísticas lexicais são reconstruídas na busca.

## 4. Algoritmo de recuperação

Dada a pergunta `Q`, para cada trecho `D`:

1. Tokeniza Q e D e conta frequências `tf(t,D)`.
2. Calcula `df(t)`, número de trechos onde o termo aparece, e `N`, total de trechos.
3. Para cada termo compartilhado calcula IDF suavizada:

```text
idf(t) = ln(1 + (N - df(t) + 0,5) / (df(t) + 0,5))
```

4. Calcula uma pontuação tipo BM25 simplificada, com frequência saturada e normalização suave pelo tamanho do trecho:

```text
léxico = Σ idf(t) · (tf(t,D) · 2,2) /
         (tf(t,D) + 1,2 · (0,25 + 0,75 · |D| / 35))
```

Aqui `|D|` é o número de tokens do trecho. O índice 35 é uma referência de escala fixa, não uma estatística treinada por corpus.

5. Calcula cobertura da consulta: `termos distintos compartilhados / termos distintos da consulta`.
6. Adiciona bônus de frase exata quando a pergunta normalizada (com pelo menos quatro caracteres) aparece no trecho.
7. Calcula a proporção de bigramas consecutivos coincidentes.
8. Calcula similaridade de cosseno entre contagens de categorias ParteB da pergunta e do trecho.
9. Soma os sinais com estes pesos da versão atual:

```text
pontuação = léxico
          + 1,25 × cobertura
          + 2,00 × frase_exata
          + 0,35 × continuidade_de_bigramas
          + 0,20 × similaridade_de_categorias
```

10. Ordena por maior pontuação, depois por menor comprimento e por fonte em ordem estável. Só trechos com ao menos um termo compartilhado entram nos resultados.

Os pesos são heurísticos e foram escolhidos para priorizar conteúdo lexical e cobertura, mantendo ParteB como sinal auxiliar. Não são parâmetros ajustados num conjunto de avaliação. Se nenhum trecho compartilha palavras com a pergunta, a resposta é explicitamente “não encontrei”; não há fallback especulativo.

## 5. Composição da resposta

`BaseAprendizado.responder(pergunta)` busca até três candidatos. Quando há resultado, devolve:

- `resposta`: texto original do trecho mais bem ranqueado;
- `fonte_principal`: caminho do documento que forneceu o trecho;
- `pontuacao`: valor de ordenação (não probabilidade);
- `fontes`: fontes únicas associadas aos candidatos;
- `alternativas`: outros trechos próximos.

Sem candidatos, retorna `encontrado=False`, mensagem de ausência de correspondência e fontes vazias. O subpacote `NovosSistemas/interacao/` oferece uma API reutilizável e uma sessão de perguntas sucessivas; `NovosSistemas/chatbot/` acrescenta uma apresentação conversacional sobre a mesma API. Ambas repetem este comportamento até `/sair`, `sair`, `tchau` ou `fim`.

## 6. Persistência e versão

A base é JSON UTF-8 com número de versão, arrays alinhados ParteA/ParteB, documentos e trechos. A escrita ocorre num arquivo temporário no mesmo diretório e é finalizada por substituição atômica. A leitura recusa versão desconhecida, mapa ParteA/ParteB divergente ou trecho incompleto. Não há execução de conteúdo contido dentro do JSON.

Caminho padrão: `NovosSistemas/dados/base_aprendizado.json`. `--modelo CAMINHO` escolhe outro arquivo.

## 7. Pseudocódigo ponta a ponta

```text
APRENDER(arquivos, base):
    para cada arquivo escolhido:
        texto ← EXTRAIR_TEXTO(arquivo)
        segmentos ← DIVIDIR_POR_PARAGRAFOS_E_FRASES(texto)
        para segmento em segmentos:
            id ← SHA256(caminho + NUL + NORMALIZAR(segmento))
            se id ainda não existe:
                salvar {id, texto original, caminho de origem}
    SALVAR_JSON_ATOMICAMENTE(base)

RESPONDER(pergunta, base):
    termos ← TOKENIZAR(NORMALIZAR(pergunta))
    se termos vazios ou base sem trechos:
        retornar “não encontrado”
    para cada trecho:
        termos_trecho ← TOKENIZAR(trecho)
        se termos sem interseção com termos_trecho:
            continuar
        calcular IDF, BM25 simplificado, cobertura, frase, bigramas e ParteB
        pontuação ← soma ponderada descrita acima
    ordenar candidatos por pontuação decrescente
    se lista vazia:
        retornar “não encontrado”
    retornar trecho #1, caminho da fonte e candidatos alternativos
```

## 8. Segurança, privacidade e limitações

- Os arquivos são processados na máquina/ambiente onde o código é executado; não há envio a APIs.
- O extrator HTML ignora script e estilo. Arquivos Office abertos são lidos como XML, sem macros.
- `.doc`, `.ppt`, `.xls` legados são delegados a ferramentas locais opcionais; use conversores atualizados e documentos confiáveis.
- O chatbot não valida fatos externos nem resolve sinônimos de forma semântica. Para maior recall, aprenda documentos pertinentes e faça perguntas com termos usados nos textos.
- PDFs escaneados, imagens, áudio/vídeo e documentos protegidos por senha exigem OCR/conversão prévia.
- A associação numérica ParteB é explicável, mas categorias de caractere sozinhas não carregam semântica de linguagem.

## 9. Testes

```bash
python -m unittest discover -s NovosSistemas/tests -v
```

Os testes verificam o alinhamento ParteA/ParteB, classificação Unicode, recuperação com fonte, resposta vazia sem conteúdo correspondente, deduplicação, persistência, TXT/CSV/HTML/JSON/RTF/DOCX/EPUB e seleção numérica.
