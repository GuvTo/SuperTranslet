"""Chatbot leve: conversa em português usando respostas recuperadas da base local."""
from __future__ import annotations

from pathlib import Path

from ..aprendizado.modelo import BaseAprendizado, carregar_ou_nova
from ..interacao.respostas import InteracaoAprendida


class ChatbotAprendido:
    """Fachada de conversa que reutiliza a API de interação/aprendizado."""

    def __init__(self, base: BaseAprendizado | None = None) -> None:
        self.interacao = InteracaoAprendida(base=base if base is not None else BaseAprendizado())

    def responder(self, pergunta: str) -> dict:
        """Devolve trecho relevante, alternativas e fontes com base no material treinado."""
        pergunta = pergunta.strip()
        if not pergunta:
            return {"encontrado": False, "resposta": "Escreva uma pergunta para eu consultar o material aprendido.", "fontes": [], "alternativas": []}
        return self.interacao.responder(pergunta)


def conversar(caminho_modelo: str | Path, base: BaseAprendizado | None = None) -> None:
    """Abre um ciclo de chat no terminal; use sair, tchau ou /sair para encerrá-lo."""
    modelo = base if base is not None else carregar_ou_nova(caminho_modelo)
    bot = ChatbotAprendido(modelo)
    print("Chatbot SuperTranslet — respostas limitadas aos documentos aprendidos.")
    print("Digite /sair para terminar. Para adicionar documentos, volte ao menu e escolha Aprender.")
    while True:
        try:
            pergunta = input("Você> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nConversa encerrada.")
            return
        if pergunta.casefold() in {"/sair", "sair", "tchau", "fim"}:
            print("Chatbot> Até logo.")
            return
        resultado = bot.responder(pergunta)
        print(f"Chatbot> {resultado['resposta']}")
        if resultado.get("fonte_principal"):
            print(f"Fonte: {resultado['fonte_principal']}")
        if resultado.get("alternativas"):
            print(f"(Há mais {len(resultado['alternativas'])} trecho(s) relacionado(s) na base.)")
