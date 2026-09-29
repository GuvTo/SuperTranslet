"""Leitura segura e local de formatos documentais comuns para texto pesquisável.

O módulo usa a biblioteca padrão sempre que possível. PDF e formatos binários
legados recorrem a pdftotext, antiword ou LibreOffice se instalados; nenhuma
rotina executa macros nem envia documentos para serviços externos.
"""
from __future__ import annotations

import csv
from html.parser import HTMLParser
import io
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable
import zipfile
import xml.etree.ElementTree as ET

EXTENSOES_SUPORTADAS = {
    ".txt", ".text", ".md", ".markdown", ".rst", ".log", ".csv", ".tsv",
    ".json", ".yaml", ".yml", ".html", ".htm", ".xhtml", ".xml", ".rtf",
    ".doc", ".docx", ".pdf", ".epub", ".odt", ".ods", ".odp", ".ppt",
    ".pptx", ".xls", ".xlsx",
}


class _ExtratorHTML(HTMLParser):
    """Transforma HTML em texto, ignorando marcação, scripts, estilos e metadados."""
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self._ignorar = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg", "head"}:
            self._ignorar += 1
        elif tag.lower() in {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4"}:
            self.partes.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg", "head"} and self._ignorar:
            self._ignorar -= 1
        elif tag.lower() in {"p", "div", "li", "tr", "h1", "h2", "h3", "h4"}:
            self.partes.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._ignorar and data.strip():
            self.partes.append(data.strip())


def _html_para_texto(html: str) -> str:
    """Remove tags e conteúdo executável de um fragmento HTML/XHTML."""
    parser = _ExtratorHTML()
    parser.feed(html)
    return re.sub(r"[ \t]+", " ", "\n".join(parser.partes)).strip()


def _xml_texto(conteudo: bytes) -> str:
    """Extrai nós textuais de um XML de pacote Office/OpenDocument."""
    raiz = ET.fromstring(conteudo)
    partes = [texto.strip() for texto in raiz.itertext() if texto and texto.strip()]
    return " ".join(partes)


def _ler_docx(caminho: Path) -> str:
    """Lê parágrafos e tabelas Word OOXML sem executar macros ou dependências extras."""
    with zipfile.ZipFile(caminho) as pacote:
        xml = ET.fromstring(pacote.read("word/document.xml"))
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    saida: list[str] = []
    for paragrafo in xml.iter(namespace + "p"):
        texto = "".join(no.text or "" for no in paragrafo.iter(namespace + "t"))
        if texto.strip():
            saida.append(texto)
    return "\n".join(saida)


def _ler_epub(caminho: Path) -> str:
    """Lê XHTML de um EPUB seguindo, quando disponível, a ordem do manifesto/spine."""
    with zipfile.ZipFile(caminho) as pacote:
        nomes = set(pacote.namelist())
        paginas: list[str] = []
        try:
            container = ET.fromstring(pacote.read("META-INF/container.xml"))
            rootfile = next(e.attrib["full-path"] for e in container.iter() if e.tag.endswith("rootfile"))
            opf = ET.fromstring(pacote.read(rootfile))
            base = Path(rootfile).parent
            manifest = {item.attrib["id"]: str(base / item.attrib["href"]) for item in opf.iter() if item.tag.endswith("item") and item.attrib.get("id") and item.attrib.get("href")}
            ordem = [manifest[item.attrib["idref"]] for item in opf.iter() if item.tag.endswith("itemref") and item.attrib.get("idref") in manifest]
            paginas = [nome for nome in ordem if nome in nomes]
        except (KeyError, StopIteration, ET.ParseError):
            paginas = sorted(n for n in nomes if n.lower().endswith((".xhtml", ".html", ".htm")))
        textos = []
        for pagina in paginas:
            texto = _html_para_texto(pacote.read(pagina).decode("utf-8", errors="replace"))
            if texto:
                textos.append(texto)
        return "\n\n".join(textos)


def _ler_planilha_xlsx(caminho: Path) -> str:
    """Extrai texto de células de uma planilha XLSX simples usando XML interno."""
    with zipfile.ZipFile(caminho) as pacote:
        nomes = set(pacote.namelist())
        strings: list[str] = []
        if "xl/sharedStrings.xml" in nomes:
            raiz = ET.fromstring(pacote.read("xl/sharedStrings.xml"))
            strings = ["".join(el.text or "" for el in item.iter() if el.tag.endswith("}t")) for item in raiz]
        folhas = sorted(n for n in nomes if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))
        linhas: list[str] = []
        for folha in folhas:
            raiz = ET.fromstring(pacote.read(folha))
            for linha in (e for e in raiz.iter() if e.tag.endswith("}row")):
                valores = []
                for celula in (e for e in linha if e.tag.endswith("}c")):
                    valor = next((e.text for e in celula if e.tag.endswith("}v")), "") or ""
                    if celula.attrib.get("t") == "s" and valor.isdigit() and int(valor) < len(strings):
                        valor = strings[int(valor)]
                    valores.append(valor)
                if any(valores):
                    linhas.append("\t".join(valores))
        return "\n".join(linhas)


def _ler_pptx(caminho: Path) -> str:
    """Extrai texto de slides PPTX em ordem numérica."""
    with zipfile.ZipFile(caminho) as pacote:
        nomes = sorted((n for n in pacote.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.search(r"slide(\d+)", n).group(1)))
        return "\n".join(_xml_texto(pacote.read(nome)) for nome in nomes)


def _ler_pdf(caminho: Path) -> str:
    """Extrai texto de PDF com pdftotext ou pypdf; PDFs somente imagem precisam de OCR externo."""
    executavel = shutil.which("pdftotext")
    if executavel:
        processo = subprocess.run([executavel, "-layout", str(caminho), "-"], capture_output=True, text=True, timeout=120)
        if processo.returncode == 0 and processo.stdout.strip():
            return processo.stdout.strip()
    try:
        from pypdf import PdfReader  # dependência opcional
        return "\n".join((pagina.extract_text() or "") for pagina in PdfReader(str(caminho)).pages).strip()
    except ImportError as erro:
        raise RuntimeError("PDF sem texto extraível: instale pypdf ou pdftotext; PDF digitalizado requer OCR.") from erro


def _ler_legado_com_office(caminho: Path) -> str:
    """Converte formatos binários antigos com antiword/LibreOffice, sem abrir macros."""
    antiword = shutil.which("antiword") if caminho.suffix.lower() == ".doc" else None
    if antiword:
        proc = subprocess.run([antiword, str(caminho)], capture_output=True, text=True, timeout=120)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    libreoffice = shutil.which("libreoffice") or shutil.which("soffice")
    if libreoffice:
        with tempfile.TemporaryDirectory(prefix="supertranslet-conversao-") as pasta:
            proc = subprocess.run([libreoffice, "--headless", "--convert-to", "txt:Text", "--outdir", pasta, str(caminho)], capture_output=True, text=True, timeout=120)
            convertido = Path(pasta) / (caminho.stem + ".txt")
            if proc.returncode == 0 and convertido.is_file():
                return convertido.read_text(encoding="utf-8", errors="replace").strip()
    raise RuntimeError(f"Não há conversor disponível para {caminho.suffix}; instale LibreOffice" + (" ou antiword." if caminho.suffix.lower() == ".doc" else "."))


def ler_documento(caminho: str | Path) -> str:
    """Lê um arquivo suportado e devolve texto UTF-8; informa claramente erros e formatos vazios."""
    caminho = Path(caminho).expanduser()
    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    ext = caminho.suffix.lower()
    if ext not in EXTENSOES_SUPORTADAS:
        raise ValueError(f"Formato não suportado: {ext or '(sem extensão)'}. Consulte EXTENSOES_SUPORTADAS.")
    if ext in {".txt", ".text", ".md", ".markdown", ".rst", ".log", ".yaml", ".yml"}:
        texto = caminho.read_text(encoding="utf-8-sig", errors="replace")
    elif ext in {".csv", ".tsv"}:
        delimitador = "\t" if ext == ".tsv" else ","
        with caminho.open("r", encoding="utf-8-sig", errors="replace", newline="") as arquivo:
            texto = "\n".join("\t".join(celulas) for celulas in csv.reader(arquivo, delimiter=delimitador))
    elif ext == ".json":
        objeto = json.loads(caminho.read_text(encoding="utf-8-sig"))
        texto = json.dumps(objeto, ensure_ascii=False, indent=2)
    elif ext in {".html", ".htm", ".xhtml"}:
        texto = _html_para_texto(caminho.read_text(encoding="utf-8-sig", errors="replace"))
    elif ext == ".xml":
        texto = _xml_texto(caminho.read_bytes())
    elif ext == ".rtf":
        bruto = caminho.read_text(encoding="latin-1", errors="replace")
        texto = re.sub(r"\\'[0-9a-fA-F]{2}", " ", bruto)
        texto = re.sub(r"\\[a-zA-Z]+-?\d* ?|[{}]", " ", texto)
        texto = re.sub(r"\\\\", lambda _: "\\", texto).strip()
    elif ext == ".docx":
        texto = _ler_docx(caminho)
    elif ext == ".epub":
        texto = _ler_epub(caminho)
    elif ext == ".pdf":
        texto = _ler_pdf(caminho)
    elif ext == ".xlsx":
        texto = _ler_planilha_xlsx(caminho)
    elif ext in {".pptx"}:
        texto = _ler_pptx(caminho)
    elif ext in {".odt", ".ods", ".odp"}:
        with zipfile.ZipFile(caminho) as pacote:
            xml_nome = "content.xml"
            texto = _xml_texto(pacote.read(xml_nome))
    elif ext in {".doc", ".ppt", ".xls"}:
        texto = _ler_legado_com_office(caminho)
    else:
        raise ValueError(f"Leitor ainda não implementado para {ext}")
    if not texto.strip():
        raise ValueError(f"Nenhum texto extraível em {caminho}; arquivos digitalizados precisam de OCR.")
    return texto.strip()


def listar_documentos(diretorio: str | Path, recursivo: bool = True) -> list[Path]:
    """Lista arquivos de extensões suportadas, em ordem estável, para menu numérico."""
    diretorio = Path(diretorio).expanduser()
    if not diretorio.is_dir():
        raise NotADirectoryError(f"Diretório não encontrado: {diretorio}")
    iterador: Iterable[Path] = diretorio.rglob("*") if recursivo else diretorio.glob("*")
    return sorted((p for p in iterador if p.is_file() and p.suffix.lower() in EXTENSOES_SUPORTADAS), key=lambda p: str(p).casefold())
