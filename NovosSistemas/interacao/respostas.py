"""API de interação com o conhecimento aprendido, separada da casca de chatbot."""
from __future__ import annotations

from pathlib import Path

from ..aprendizado.modelo import BaseAprendizado, carregar_ou_nova

CAMINHO_MODELO_PADRAO = Path(__file__).resolve().parents[1] / "dados" / "base_aprendizado.json"


class InteracaoAprendida:
    """Fachada síncrona que traduz perguntas para respostas do algoritmo local."""

    def __init__(self, base: BaseAprendizado | None = None, caminho_modelo: str | Path | None = None) -> None:
        self.base = base if base is not None else carregar_ou_nova(caminho_modelo or CAMINHO_MODELO_PADRAO)

    def responder(self, pergunta: str, limite: int = 3) -> dict:
        """Devolve a resposta que pode ser comprovada por trechos na base local."""
        if not pergunta.strip():
            return {
                "encontrado": False,
                "resposta": "Pergunta vazia. Escreva algo para consultar o material aprendido.",
                "fontes": [],
                "alternativas": [],
            }
        return self.base.responder(pergunta, limite=limite)

    def executar_sessao(self) -> None:
        """Executa perguntas sucessivas; encerra com /sair, sair, tchau ou fim."""
        print("Interação com o aprendizado local. Digite /sair para encerrar.")
        while True:
            try:
                pergunta = input("Pergunta> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nSessão encerrada.")
                return
            if pergunta.casefold() in {"/sair", "sair", "tchau", "fim"}:
                print("Sessão de interação encerrada.")
                return
            resultado = self.responder(pergunta)
            print(f"Resposta> {resultado['resposta']}")
            if resultado.get("fonte_principal"):
                print(f"Fonte: {resultado['fonte_principal']}")


def responder(pergunta: str, base: BaseAprendizado | None = None, caminho_modelo: str | Path | None = None) -> dict:
    """Função curta para integrar o algoritmo de resposta em outros programas Python."""
    return InteracaoAprendida(base=base, caminho_modelo=caminho_modelo).responder(pergunta)
