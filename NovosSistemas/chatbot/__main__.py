"""Ponto de entrada do chatbot: python -m NovosSistemas.chatbot."""
from pathlib import Path

from ..cli.cli import MODELO_PADRAO
from .chatbot import conversar

if __name__ == "__main__":
    conversar(Path(MODELO_PADRAO))
