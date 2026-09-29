# Interação com o aprendizado

Este subpacote separa a pergunta/resposta da interface de chatbot e da linha de comando. O arquivo `respostas.py` define `InteracaoAprendida`, uma API simples que recebe uma base carregada ou o caminho do JSON aprendido.

```python
from NovosSistemas.interacao import InteracaoAprendida

sistema = InteracaoAprendida(caminho_modelo="NovosSistemas/dados/base_aprendizado.json")
resultado = sistema.responder("O que o material diz sobre ParteA?")
print(resultado["resposta"])
print(resultado.get("fonte_principal"))
```

Para perguntas sucessivas no terminal, use `sistema.executar_sessao()` ou `python -m NovosSistemas.cli --modo interacao`. A sessão é delimitada ao conteúdo aprendido e imprime a fonte quando existe correspondência. Para uma conversa com apresentação de chatbot, utilize `NovosSistemas/chatbot/`.
