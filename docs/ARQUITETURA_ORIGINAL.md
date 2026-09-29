# Arquitetura e inventário do código original

O repositório recebido contém um ponto de entrada de exemplo e vários experimentos em Python, não uma aplicação já integrada. Esta cópia mantém caminhos e comandos executáveis. A documentação dos próprios módulos foi acrescentada em português; esta página complementa o inventário.

## Ponto de entrada

- `main.py`: modelo mínimo gerado pelo PyCharm. `print_hi(nome)` imprime uma saudação e o bloco principal passa `PyCharm`. Não chama os demais diretórios.

## SuperBrain — interpretação, aprendizado e operação

- `SuperBrain/SuperCerebro/Interpretacao/Edx/Adx/Ewx.py`: tokenizador simples, reconhece espaços, palavras alfabéticas, números, símbolos e marcadores `_:ordem`/`_:final`. Usa identificadores aleatórios e não constitui um parser gramatical.
- `.../Adx/Text.py`: outra catalogação com estados e diagnósticos no terminal; usa aleatoriedade e contém ramificações de protótipo.
- `.../Axov/Linz.py`: compara caracteres de entrada com listas fornecidas como ParteA e ParteB e agrega atributos dos tokens. O mapeamento depende das strings de entrada e não é validado no original.
- `.../Adx/AsxDew.py`: demonstração tabular/estatística que imprime estrutura e JSON; não monta uma aplicação de treinamento reutilizável.
- `SuperBrain/SuperCerebro/Aprender/Edx/Lox/Zsx.py`: importa Linz, segmenta e calcula médias dos valores de um atributo indicado; sua demonstração contém dados de exemplo.
- `.../Aprender/Edx/Adx/Asx.py`: exemplo separado de DataFrame, contagem de categorias, KNN e visualização. Usa pandas, NumPy, Matplotlib, seaborn e scikit-learn.
- `SuperBrain/SuperCerebro/Operacao/Edx/Adx/Punk.py`: protótipo de comparação numérica entre exemplos e consulta, selecionando candidatos de texto.
- `.../Adx/Gert.py`: invólucro de respostas múltiplas que chama Punk.
- `.../AdxTest/GertTest.py`: script de demonstração, não uma suíte unittest.

**Observações técnicas observadas:** imports dependem da estrutura de pastas raiz; certas funções assumem dados não vazios ou comprimentos compatíveis; há prints de debug. Os arquivos foram documentados, não corrigidos.

## Exwex — análise e gráficos de símbolos

- `Exwex/Adx/Edx/Opx/Lax.py`, `Glux.py`, `Glax.py`, `Erx.py`, `Drix.py`: variantes do processamento de respostas/símbolos, médias móveis, probabilidades e gráficos. Há diferenças entre versão e versão; nomes iguais não implicam implementação idêntica.
- `Exwex/Adx/Edx/Opx/Drix_GeralDex.py`: analisador multilíngue com argumentos CLI, cálculo de EMA/MACD, desenho/salvamento de imagem e JSON, além de handler SIGINT registrado no import.
- `Exwex/Adx/Edx/Opx/Lizx.py`: interface interativa, traduções para seis idiomas, validação, parâmetros de indicadores, arquivos CSV/gráfico/configuração e estado de emergência.
- `Exwex/Adx/Edx/Opx/resultados/`: CSVs, PNGs, JSON de configurações e histórico que já acompanhavam o snapshot.
- `Exwex/Adx/Edx/Opx/adex_file_imagem_erx744448712edx.png`: imagem de resultado existente no snapshot.
- `Exwex/Lix/Backups/BackupsUp/Upx1/...`: versões arquivadas de `Erx.py`, `Glux.py` e `Lax.py`; permanecem no lugar e não são carregadas pela extensão nova.

As rotinas de gráficos trazem código experimental, dependências científicas e algumas suposições de tamanhos. O documento não as apresenta como classificadores validados.

## SuperTradutor e UltraBrain

- `SuperTradutor/Tradutor/Cofing/Traduzir/Edk/Asx/Gex/Zsx.py`: fórmula de geração de sequência numérica e escrita de um arquivo no diretório de execução. Apesar de nomes que mencionam primos, não foi demonstrada verificação de primalidade.
- `SuperTradutor/.../primos_edk_*.txt`: arquivos numéricos que já pertenciam ao repositório; foram mantidos e não são usados pela nova base de conhecimento.
- `UltraBrain/Edx/Adx/Opx/Lox/Zsx.py`: arquivo Python vazio no snapshot.

## Configuração e dados

- `.idea/`: metadados de projeto do IDE mantidos como recebidos.
- `LICENSE`: texto da GNU GPL v3 mantido sem alteração.
- Arquivos `.csv`, `.json`, `.png`, `.txt` e bytecode `.pyc` foram mantidos no snapshot. Não são automaticamente interpretados como documentação de código.

## Extensão nova (separada)

`NovosSistemas/` é uma adição; separa o núcleo (`aprendizado/`), a API de perguntas (`interacao/`), o chatbot (`chatbot/`), a CLI (`cli/`) e testes (`tests/`). Não substitui imports nem scripts do inventário acima. O fluxo de aprendizado e resposta está especificado em `ALGORITMO_APRENDIZADO_E_RESPOSTA.md`; os formatos são descritos em `FORMATOS_E_LIMITACOES.md`.
