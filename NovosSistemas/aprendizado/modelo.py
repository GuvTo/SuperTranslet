"""Motor independente de aprendizado e respostas do SuperTranslet.

O motor preserva a ideia ParteA/ParteB do projeto original: ParteA contém
caracteres e ParteB contém um inteiro alinhado a cada caractere. A camada
nova usa os grupos como atributos explicáveis, indexa trechos dos documentos,
calcula pesos lexicais e recupera conteúdo relevante, sem inventar fatos.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import tempfile
import unicodedata
from typing import Any

# Os números são categorias (não posições nem probabilidades). Cada símbolo
# de PARTE_A ocupa a mesma posição que seu código de categoria em PARTE_B.
GRUPOS_PARTE_A_B: tuple[tuple[int, str, str], ...] = (
    (1, "letras maiúsculas", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    (2, "letras minúsculas", "abcdefghijklmnopqrstuvwxyz"),
    (3, "algarismos", "0123456789"),
    (4, "operadores", "+-*/^%="),
    (5, "pontuação", ".,?!;:"),
    (6, "espaços em branco", " \t\n\r"),
    (7, "delimitadores e outros sinais", "_[]{}()<>\\|@#$&~`\"'"),
)
PARTE_A: tuple[str, ...] = tuple(caractere for _, _, chars in GRUPOS_PARTE_A_B for caractere in chars)
PARTE_B: tuple[int, ...] = tuple(codigo for codigo, _, chars in GRUPOS_PARTE_A_B for _ in chars)
if len(PARTE_A) != len(PARTE_B) or len(set(PARTE_A)) != len(PARTE_A):
    raise RuntimeError("ParteA e ParteB precisam ter o mesmo tamanho e caracteres únicos")
MAPA_CARACTERE_NUMERO: dict[str, int] = dict(zip(PARTE_A, PARTE_B))
VERSAO_MODELO = 1

_TOKEN_RE = re.compile(r"[^\W_]+", flags=re.UNICODE)
_PARAGRAFO_RE = re.compile(r"\n\s*\n+")
_FRASE_RE = re.compile(r"(?<=[.!?])\s+|\s*[•▪]\s+")


def normalizar(texto: str) -> str:
    """Padroniza Unicode e caixa para comparação, mantendo acentos e conteúdo original."""
    return unicodedata.normalize("NFKC", texto).casefold().strip()


def tokenizar(texto: str) -> list[str]:
    """Extrai palavras Unicode para o índice lexical; sinais isolados não viram termos."""
    return _TOKEN_RE.findall(normalizar(texto))


def classificar_caractere(caractere: str) -> int:
    """Retorna o número ParteB associado ao caractere ParteA ou 0 para desconhecidos."""
    if not caractere:
        return 0
    conhecido = MAPA_CARACTERE_NUMERO.get(caractere)
    if conhecido is not None:
        return conhecido
    # Extensão determinística para alfabetos Unicode fora do alfabeto ASCII inicial.
    if caractere.isalpha():
        return 1 if caractere.isupper() else 2
    if caractere.isnumeric():
        return 3
    if caractere.isspace():
        return 6
    return 0


def codificar_texto(texto: str) -> list[int]:
    """Converte cada caractere em seu código de grupo ParteB, na ordem original."""
    return [classificar_caractere(c) for c in texto]


def perfil_caracteres(texto: str) -> Counter[int]:
    """Conta os códigos numéricos ParteB presentes no texto, ignorando desconhecidos."""
    return Counter(codigo for codigo in codificar_texto(texto) if codigo)


def _dividir_em_trechos(texto: str, limite: int = 1200) -> list[str]:
    """Divide um documento em unidades de resposta com pontuação e limite de tamanho."""
    resultado: list[str] = []
    for paragrafo in _PARAGRAFO_RE.split(texto.replace("\r\n", "\n").replace("\r", "\n")):
        paragrafo = re.sub(r"\s+", " ", paragrafo).strip()
        if not paragrafo:
            continue
        frases = [f.strip() for f in _FRASE_RE.split(paragrafo) if f.strip()]
        buffer = ""
        for frase in frases or [paragrafo]:
            if len(frase) > limite:
                palavras = frase.split()
                for palavra in palavras:
                    if buffer and len(buffer) + len(palavra) + 1 > limite:
                        resultado.append(buffer)
                        buffer = ""
                    buffer = f"{buffer} {palavra}".strip()
            elif buffer and len(buffer) + len(frase) + 1 > limite:
                resultado.append(buffer)
                buffer = frase
            else:
                buffer = f"{buffer} {frase}".strip()
        if buffer:
            resultado.append(buffer)
    return resultado


def _similaridade_cosseno(a: Counter[int], b: Counter[int]) -> float:
    """Calcula similaridade de cosseno entre frequências de categorias ParteB."""
    if not a or not b:
        return 0.0
    produto = sum(valor * b.get(chave, 0) for chave, valor in a.items())
    norma_a = math.sqrt(sum(valor * valor for valor in a.values()))
    norma_b = math.sqrt(sum(valor * valor for valor in b.values()))
    return produto / (norma_a * norma_b) if norma_a and norma_b else 0.0


@dataclass(frozen=True)
class ResultadoBusca:
    """Trecho ranqueado, fonte e pontuação normalizada para exibição ou testes."""
    texto: str
    fonte: str
    pontuacao: float

    def como_dict(self) -> dict[str, Any]:
        """Converte o resultado em estrutura simples serializável/compatível com CLI."""
        return {"texto": self.texto, "fonte": self.fonte, "pontuacao": round(self.pontuacao, 6)}


class BaseAprendizado:
    """Índice local de trechos aprendidos, metadados de arquivos e mapeamento ParteA/B."""

    def __init__(self) -> None:
        self.trechos: list[dict[str, str]] = []
        self.documentos: list[dict[str, Any]] = []
        self._ids_trechos: set[str] = set()
        self._ids_documentos: set[str] = set()

    @property
    def quantidade_documentos(self) -> int:
        """Número de documentos distintos incorporados à base atual."""
        return len(self.documentos)

    @property
    def quantidade_trechos(self) -> int:
        """Número de trechos únicos indexados na base atual."""
        return len(self.trechos)

    def aprender_texto(self, texto: str, fonte: str = "(texto informado)") -> int:
        """Indexa os trechos de um texto e devolve quantos trechos novos foram adicionados.

        Cada trecho mantém a fonte original. Repetir o mesmo arquivo não duplica
        registros: a identidade do trecho considera fonte e conteúdo normalizado.
        """
        texto = texto.strip()
        if not texto:
            return 0
        digest_doc = hashlib.sha256((str(fonte) + "\0" + normalizar(texto)).encode("utf-8")).hexdigest()
        if digest_doc not in self._ids_documentos:
            self.documentos.append({"fonte": str(fonte), "sha256": digest_doc, "caracteres": len(texto)})
            self._ids_documentos.add(digest_doc)
        novos = 0
        for trecho in _dividir_em_trechos(texto):
            digest = hashlib.sha256((str(fonte) + "\0" + normalizar(trecho)).encode("utf-8")).hexdigest()
            if digest in self._ids_trechos:
                continue
            self.trechos.append({"id": digest, "texto": trecho, "fonte": str(fonte)})
            self._ids_trechos.add(digest)
            novos += 1
        return novos

    def aprender_arquivo(self, caminho: str | Path) -> int:
        """Lê e indexa um arquivo com o leitor multimídia do pacote."""
        from .leitores import ler_documento
        caminho = Path(caminho).expanduser().resolve()
        return self.aprender_texto(ler_documento(caminho), str(caminho))

    def buscar(self, pergunta: str, limite: int = 3) -> list[dict[str, Any]]:
        """Ranqueia trechos por relevância lexical, frase, sequência e categoria de caracteres.

        O ranqueamento é inteiramente local e determinístico. O IDF reduz o peso
        de termos comuns; cobertura e frase exata favorecem correspondências
        específicas; os grupos ParteB fornecem um sinal auxiliar, nunca substituem
        o conteúdo lexical. Retorna uma lista vazia quando não há correspondência.
        """
        termos = tokenizar(pergunta)
        if not termos or not self.trechos or limite <= 0:
            return []
        consulta = normalizar(pergunta)
        q_counts = Counter(termos)
        q_unicos = set(termos)
        n = len(self.trechos)
        doc_freq: Counter[str] = Counter()
        preparados: list[tuple[dict[str, str], list[str], Counter[str]]] = []
        for trecho in self.trechos:
            toks = tokenizar(trecho["texto"])
            tf = Counter(toks)
            doc_freq.update(set(toks))
            preparados.append((trecho, toks, tf))
        q_perfil = perfil_caracteres(pergunta)
        pontuados: list[ResultadoBusca] = []
        for registro, toks, tf in preparados:
            presentes = q_unicos.intersection(tf)
            if not presentes:
                continue
            # BM25 simplificado: frequência saturada e penalização suave por extensão.
            tamanho = max(1, len(toks))
            soma = 0.0
            for termo in presentes:
                idf = math.log(1 + (n - doc_freq[termo] + 0.5) / (doc_freq[termo] + 0.5))
                freq = tf[termo]
                soma += idf * (freq * 2.2) / (freq + 1.2 * (0.25 + 0.75 * tamanho / 35))
            cobertura = len(presentes) / max(1, len(q_unicos))
            texto_norm = normalizar(registro["texto"])
            frase_exata = 1.0 if len(consulta) >= 4 and consulta in texto_norm else 0.0
            bigramas_q = set(zip(termos, termos[1:]))
            bigramas_t = set(zip(toks, toks[1:]))
            continuidade = len(bigramas_q & bigramas_t) / max(1, len(bigramas_q))
            categoria = _similaridade_cosseno(q_perfil, perfil_caracteres(registro["texto"]))
            bruto = soma + 1.25 * cobertura + 2.0 * frase_exata + 0.35 * continuidade + 0.2 * categoria
            pontuados.append(ResultadoBusca(registro["texto"], registro["fonte"], bruto))
        pontuados.sort(key=lambda r: (-r.pontuacao, len(r.texto), r.fonte.casefold()))
        return [item.como_dict() for item in pontuados[:limite]]

    def responder(self, pergunta: str, limite: int = 3) -> dict[str, Any]:
        """Responde com o trecho mais relevante e as fontes verificáveis da busca."""
        resultados = self.buscar(pergunta, limite=limite)
        if not resultados:
            return {
                "encontrado": False,
                "resposta": "Não encontrei uma resposta correspondente no material aprendido. Aprenda documentos relacionados e tente novamente.",
                "fontes": [],
                "alternativas": [],
            }
        principal = resultados[0]
        fontes = list(dict.fromkeys(r["fonte"] for r in resultados))
        return {
            "encontrado": True,
            "resposta": principal["texto"],
            "fonte_principal": principal["fonte"],
            "pontuacao": principal["pontuacao"],
            "fontes": fontes,
            "alternativas": resultados[1:],
        }

    def salvar(self, caminho: str | Path) -> Path:
        """Grava base e metadados em JSON UTF-8 por substituição atômica."""
        destino = Path(caminho).expanduser()
        destino.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "versao": VERSAO_MODELO,
            "descricao": "Índice lexical local com categorias ParteA/ParteB",
            "parte_a": list(PARTE_A),
            "parte_b": list(PARTE_B),
            "documentos": self.documentos,
            "trechos": self.trechos,
        }
        temporario: Path | None = None
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=destino.parent, delete=False) as arquivo:
                json.dump(payload, arquivo, ensure_ascii=False, indent=2)
                temporario = Path(arquivo.name)
            temporario.replace(destino)
        finally:
            if temporario and temporario.exists():
                temporario.unlink()
        return destino

    @classmethod
    def carregar(cls, caminho: str | Path) -> "BaseAprendizado":
        """Carrega e valida uma base JSON previamente salva."""
        origem = Path(caminho).expanduser()
        payload = json.loads(origem.read_text(encoding="utf-8"))
        if payload.get("versao") != VERSAO_MODELO:
            raise ValueError(f"Versão de base não suportada: {payload.get('versao')!r}")
        if payload.get("parte_a") != list(PARTE_A) or payload.get("parte_b") != list(PARTE_B):
            raise ValueError("O mapeamento ParteA/ParteB salvo não corresponde ao mapeamento desta versão")
        instancia = cls()
        instancia.documentos = list(payload.get("documentos", []))
        instancia.trechos = list(payload.get("trechos", []))
        instancia._ids_documentos = {str(d.get("sha256")) for d in instancia.documentos if d.get("sha256")}
        instancia._ids_trechos = {str(t.get("id")) for t in instancia.trechos if t.get("id")}
        if any(not all(k in t for k in ("id", "texto", "fonte")) for t in instancia.trechos):
            raise ValueError("A base contém um trecho incompleto")
        return instancia


def carregar_ou_nova(caminho: str | Path) -> BaseAprendizado:
    """Abre a base existente ou cria uma nova quando o caminho ainda não existe."""
    caminho = Path(caminho).expanduser()
    return BaseAprendizado.carregar(caminho) if caminho.is_file() else BaseAprendizado()
