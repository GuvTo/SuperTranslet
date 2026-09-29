# Formatos de documentos e condições de leitura

O leitor fica em `NovosSistemas/aprendizado/leitores.py`. A extração acontece localmente e produz texto para indexação. O código não executa macros e não faz OCR.

| Formato/extensão | Estado | Método / observação |
|---|---|---|
| `.txt`, `.text`, `.md`, `.markdown`, `.rst`, `.log` | Suportado | UTF-8; erros inválidos de byte são substituídos. |
| `.csv`, `.tsv` | Suportado | Lê linhas e preserva colunas separadas por tabulação. |
| `.json` | Suportado | Analisa JSON e serializa o objeto em texto legível. |
| `.yaml`, `.yml` | Suportado | Indexa como texto; não interpreta tags/âncoras YAML. |
| `.html`, `.htm`, `.xhtml` | Suportado | Remove marcação, script, estilo e conteúdo de head. |
| `.xml` | Suportado | Extrai nós textuais XML bem formado. |
| `.rtf` | Suporte básico | Remove comandos de formatação comuns; conversão complexa pode perder detalhes. |
| `.docx` | Suportado | Lê OOXML com ZIP/XML; texto de parágrafos e tabelas. |
| `.pdf` | Suportado se houver extrator | `pdftotext` preferencial; alternativa opcional `pypdf`. PDF escaneado sem camada textual exige OCR externo. |
| `.epub` | Suportado | Lê capítulos XHTML em ordem do spine quando disponível. |
| `.odt`, `.ods`, `.odp` | Suportado | Extrai texto do `content.xml` interno. |
| `.pptx` | Suportado | Lê texto XML dos slides, em ordem numérica. |
| `.xlsx` | Suportado | Lê células compartilhadas e valores das planilhas OOXML. |
| `.doc`, `.ppt`, `.xls` legados | Condicional | Requer `antiword` para `.doc` ou LibreOffice (`soffice`) para conversão local. Sem a ferramenta, explica como habilitar suporte. |

## Instalação opcional

Para PDF, basta instalar `poppler-utils` (inclui `pdftotext`) ou instalar a biblioteca `pypdf` no mesmo ambiente Python. Para Office legado, instale LibreOffice; `antiword` pode ser usado especificamente para `.doc`.

## Itens que ainda exigem tratamento externo

- PDFs escaneados, fotografias e imagens dentro dos documentos: OCR prévio.
- Arquivos protegidos por senha, truncados ou malformados: remover a proteção/consertar antes de aprender.
- `.docm`, `.xlsm`, formatos proprietários e áudio/vídeo: não fazem parte da lista suportada. Não execute macros; converta uma cópia para formato aberto/texto antes de usar.
- A extração preserva texto, não necessariamente paginação, colunas, fórmulas, notas de rodapé, imagens ou layout visual.
