"""Interface CLI mestre: seleciona modo, arquivos por caminho ou número e base local."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from ..aprendizado.leitores import EXTENSOES_SUPORTADAS, listar_documentos
from ..aprendizado.modelo import BaseAprendizado, PARTE_A, PARTE_B, carregar_ou_nova
from ..chatbot.chatbot import conversar
from ..interacao.respostas import InteracaoAprendida

PASTA_PACOTE = Path(__file__).resolve().parents[1]
MODELO_PADRAO = PASTA_PACOTE / "dados" / "base_aprendizado.json"


def selecionar_documentos_numericos(arquivos: list[Path], selecao: str) -> list[Path]:
    """Converte números (1,3) ou 'todos' em arquivos; índices mostrados começam em 1."""
    selecao = selecao.strip().casefold()
    if selecao in {"todos", "t", "all", "*"}:
        return list(arquivos)
    try:
        indices = [int(p.strip()) for p in selecao.split(",") if p.strip()]
    except ValueError as erro:
        raise ValueError("Informe números separados por vírgula, 'todos' ou um caminho.") from erro
    if not indices:
        raise ValueError("Nenhum número de arquivo foi informado.")
    if len(set(indices)) != len(indices):
        indices = list(dict.fromkeys(indices))
    if any(indice < 1 or indice > len(arquivos) for indice in indices):
        raise ValueError(f"Escolha números entre 1 e {len(arquivos)}.")
    return [arquivos[indice - 1] for indice in indices]


def _escolher_arquivos(args: argparse.Namespace) -> list[Path]:
    """Resolve arquivos explícitos, uma escolha numérica ou todos os itens de um diretório."""
    if args.arquivo:
        caminhos = [Path(nome).expanduser().resolve() for nome in args.arquivo]
        for caminho in caminhos:
            if not caminho.is_file():
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
            if caminho.suffix.lower() not in EXTENSOES_SUPORTADAS:
                raise ValueError(f"Formato não suportado: {caminho.suffix}; extensões: {', '.join(sorted(EXTENSOES_SUPORTADAS))}")
        return caminhos
    diretorio = Path(args.diretorio or ".").expanduser().resolve()
    encontrados = listar_documentos(diretorio, recursivo=not args.sem_recursao)
    if not encontrados:
        raise FileNotFoundError(f"Nenhum documento suportado encontrado em {diretorio}")
    print(f"Documentos encontrados em {diretorio}:")
    for numero, caminho in enumerate(encontrados, 1):
        print(f"  {numero:>3}. {caminho.relative_to(diretorio)}")
    if args.selecionar:
        return selecionar_documentos_numericos(encontrados, args.selecionar)
    while True:
        try:
            entrada = input("Escolha número(s) (ex.: 1 ou 1,3) ou 'todos': ")
        except (EOFError, KeyboardInterrupt) as erro:
            raise RuntimeError("Seleção interrompida") from erro
        try:
            return selecionar_documentos_numericos(encontrados, entrada)
        except ValueError as erro:
            print(f"Seleção inválida: {erro}")


def _aprender(args: argparse.Namespace) -> int:
    """Lê os documentos escolhidos, incorpora trechos e persiste o índice."""
    arquivos = _escolher_arquivos(args)
    base = carregar_ou_nova(args.modelo)
    total_novos = 0
    for arquivo in arquivos:
        try:
            novos = base.aprender_arquivo(arquivo)
            total_novos += novos
            print(f"Aprendido: {arquivo} ({novos} trecho(s) novo(s))")
        except Exception as erro:
            print(f"Falha ao ler {arquivo}: {erro}", file=sys.stderr)
    destino = base.salvar(args.modelo)
    print(f"Base salva: {destino}")
    print(f"Resumo: {base.quantidade_documentos} documento(s), {base.quantidade_trechos} trecho(s), {total_novos} trecho(s) novo(s) nesta execução.")
    return 0 if total_novos or base.quantidade_trechos else 1


def _perguntar(args: argparse.Namespace) -> int:
    """Responde uma pergunta e imprime os trechos-fontes que justificam o retorno."""
    base = carregar_ou_nova(args.modelo)
    if not base.quantidade_trechos:
        print(f"A base está vazia: {args.modelo}. Use --modo aprender antes de perguntar.", file=sys.stderr)
        return 2
    pergunta = args.pergunta or input("Pergunta> ")
    resultado = InteracaoAprendida(base=base).responder(pergunta)
    print(resultado["resposta"])
    if resultado.get("fonte_principal"):
        print(f"\nFonte principal: {resultado['fonte_principal']}")
        print(f"Pontuação de relevância (heurística): {resultado['pontuacao']:.3f}")
    if resultado.get("alternativas"):
        print("\nTrechos alternativos:")
        for item in resultado["alternativas"]:
            print(f"- {item['texto']}\n  Fonte: {item['fonte']}")
    return 0 if resultado["encontrado"] else 1


def _mostrar_mapa() -> None:
    """Exibe a tabela de categorias e confirma que cada item de ParteA tem ParteB."""
    print("MAPEAMENTO ParteA → ParteB (número = categoria)")
    for caractere, numero in zip(PARTE_A, PARTE_B):
        print(f"{repr(caractere):>8} → {numero}")
    print(f"Total: {len(PARTE_A)} caracteres mapeados; {len(PARTE_B)} números alinhados.")
    print("Caracteres Unicode não listados são classificados por regra (letra, número, espaço) ou código 0.")


def _menu(args: argparse.Namespace) -> int:
    """Menu principal para selecionar aprendizado, interação, chatbot, consulta ou mapa."""
    while True:
        print("\n=== SuperTranslet — sistemas locais ===")
        print("1. Aprender com arquivo(s) (caminho ou seleção numérica)")
        print("2. Interagir em perguntas sucessivas com a base aprendida")
        print("3. Abrir chatbot sobre o aprendizado")
        print("4. Fazer uma pergunta única pela CLI")
        print("5. Ver o mapa ParteA/ParteB")
        print("6. Sair")
        try:
            escolha = input("Sistema a usar [1-6]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrado.")
            return 0
        if escolha == "1":
            try:
                _aprender(args)
            except Exception as erro:
                print(f"Não foi possível aprender: {erro}", file=sys.stderr)
        elif escolha == "2":
            InteracaoAprendida(caminho_modelo=args.modelo).executar_sessao()
        elif escolha == "3":
            conversar(args.modelo)
        elif escolha == "4":
            try:
                _perguntar(args)
            except (EOFError, KeyboardInterrupt):
                print("Pergunta cancelada.")
        elif escolha == "5":
            _mostrar_mapa()
        elif escolha == "6":
            return 0
        else:
            print("Opção inválida. Escolha um número entre 1 e 6.")


def criar_parser() -> argparse.ArgumentParser:
    """Cria os argumentos em português usados nos modos direto e interativo."""
    parser = argparse.ArgumentParser(
        prog="supertranslet",
        description="Aprendizado local ParteA/ParteB, interação, chatbot com fontes e CLI de documentos.",
        epilog="Exemplo: python -m NovosSistemas.cli --modo aprender --diretorio ./docs --selecionar 1,2",
    )
    parser.add_argument("--modo", choices=("menu", "aprender", "interacao", "chatbot", "responder", "mapa"), default="menu", help="Sistema/modo a executar")
    parser.add_argument("--modelo", type=Path, default=MODELO_PADRAO, help="Caminho do índice JSON persistente")
    parser.add_argument("--diretorio", type=Path, help="Pasta a listar para aprendizado; busca recursiva por padrão")
    parser.add_argument("--arquivo", nargs="+", help="Caminho de um ou mais arquivos para aprender")
    parser.add_argument("--selecionar", help="Número(s) da lista (ex.: 2 ou 1,3) ou 'todos'")
    parser.add_argument("--sem-recursao", action="store_true", help="Lista somente arquivos diretamente na pasta")
    parser.add_argument("--pergunta", help="Pergunta de resposta única no modo responder")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada da CLI mestre e despachante entre os sistemas novos."""
    args = criar_parser().parse_args(argv)
    try:
        if args.modo == "aprender":
            return _aprender(args)
        if args.modo == "interacao":
            InteracaoAprendida(caminho_modelo=args.modelo).executar_sessao()
            return 0
        if args.modo == "chatbot":
            conversar(args.modelo)
            return 0
        if args.modo == "responder":
            return _perguntar(args)
        if args.modo == "mapa":
            _mostrar_mapa()
            return 0
        return _menu(args)
    except (OSError, ValueError, RuntimeError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
