# Algoritmo de aprendizado

Arquivos do submódulo:

- `modelo.py`: mapeamento validado ParteA/ParteB, normalização, indexação, ranqueamento, respostas com fontes e persistência JSON.
- `leitores.py`: extração local de documentos.
- `mapeamento_parte_a_parte_b.json`: grupos e códigos numéricos legíveis.
- `../dados/exemplo_aprendizado.txt`: exemplo pequeno para teste manual.

O motor transforma cada caractere em número de categoria, mas recupera respostas principalmente por correspondência lexical ponderada e contexto de frase. A tabela ParteA/ParteB representa **tipo de caractere**, não sentido semântico. Consulte `../../docs/ALGORITMO_APRENDIZADO_E_RESPOSTA.md` para fórmulas, fluxo, pseudocódigo, persistência e limitações.
