"""Testes locais do sistema novo; execute python -m unittest discover -s NovosSistemas/tests."""
from pathlib import Path
import tempfile
import unittest
import zipfile

from NovosSistemas.aprendizado.leitores import ler_documento
from NovosSistemas.aprendizado.modelo import (
    BaseAprendizado, MAPA_CARACTERE_NUMERO, PARTE_A, PARTE_B, classificar_caractere,
)
from NovosSistemas.cli.cli import selecionar_documentos_numericos


class TestMapaParteAB(unittest.TestCase):
    def test_parte_a_e_b_tem_mesmo_comprimento_e_mapeamento_unico(self):
        self.assertEqual(len(PARTE_A), len(PARTE_B))
        self.assertEqual(len(MAPA_CARACTERE_NUMERO), len(PARTE_A))
        self.assertEqual(classificar_caractere("A"), 1)
        self.assertEqual(classificar_caractere("a"), 2)
        self.assertEqual(classificar_caractere("7"), 3)
        self.assertEqual(classificar_caractere("+"), 4)
        self.assertEqual(classificar_caractere("?"), 5)
        self.assertEqual(classificar_caractere("\n"), 6)
        self.assertEqual(classificar_caractere("_"), 7)
        self.assertEqual(classificar_caractere("ç"), 2)
        self.assertEqual(classificar_caractere("🙂"), 0)


class TestAprendizado(unittest.TestCase):
    def test_aprende_responde_e_persiste(self):
        base = BaseAprendizado()
        texto = "ParteA reúne caracteres. ParteB associa um número a cada caractere."
        adicionados = base.aprender_texto(texto, "guia.txt")
        self.assertGreaterEqual(adicionados, 1)
        resposta = base.responder("O que ParteB associa a cada caractere?")
        self.assertTrue(resposta["encontrado"])
        self.assertIn("número", resposta["resposta"])
        self.assertEqual(resposta["fonte_principal"], "guia.txt")
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "base.json"
            base.salvar(caminho)
            recarregada = BaseAprendizado.carregar(caminho)
            self.assertEqual(recarregada.quantidade_trechos, base.quantidade_trechos)
            self.assertTrue(recarregada.responder("ParteA caracteres")["encontrado"])

    def test_nao_responde_sem_termo_compativel(self):
        base = BaseAprendizado()
        base.aprender_texto("O texto fala sobre categorias de caracteres.", "arquivo.txt")
        resposta = base.responder("qual a previsão do clima em Marte?")
        self.assertFalse(resposta["encontrado"])
        self.assertEqual(resposta["fontes"], [])

    def test_repetir_mesmo_documento_nao_duplica_trechos(self):
        base = BaseAprendizado()
        texto = "Uma regra simples. Outra regra documentada."
        primeiro = base.aprender_texto(texto, "mesmo.txt")
        segundo = base.aprender_texto(texto, "mesmo.txt")
        self.assertGreater(primeiro, 0)
        self.assertEqual(segundo, 0)


class TestLeitores(unittest.TestCase):
    def test_txt_csv_html_json_e_rtf(self):
        with tempfile.TemporaryDirectory() as pasta_tmp:
            pasta = Path(pasta_tmp)
            (pasta / "a.txt").write_text("Conteúdo em português.", encoding="utf-8")
            self.assertIn("português", ler_documento(pasta / "a.txt"))
            (pasta / "a.csv").write_text("nome,valor\nParteA,4\n", encoding="utf-8")
            self.assertIn("ParteA", ler_documento(pasta / "a.csv"))
            (pasta / "a.html").write_text("<html><head><title>oculto</title></head><body><p>Texto visível</p><script>alert(1)</script></body></html>", encoding="utf-8")
            html = ler_documento(pasta / "a.html")
            self.assertIn("Texto visível", html)
            self.assertNotIn("alert", html)
            (pasta / "a.json").write_text('{"chave":"valor"}', encoding="utf-8")
            self.assertIn("valor", ler_documento(pasta / "a.json"))
            (pasta / "a.rtf").write_text(r"{\rtf1\ansi Texto RTF}", encoding="latin-1")
            self.assertIn("Texto RTF", ler_documento(pasta / "a.rtf"))

    def test_docx_e_epub(self):
        with tempfile.TemporaryDirectory() as pasta_tmp:
            pasta = Path(pasta_tmp)
            docx = pasta / "amostra.docx"
            doc_xml = '''<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Texto DOCX extraído</w:t></w:r></w:p></w:body></w:document>'''
            with zipfile.ZipFile(docx, "w") as pacote:
                pacote.writestr("word/document.xml", doc_xml)
            self.assertIn("DOCX", ler_documento(docx))
            epub = pasta / "amostra.epub"
            container = '''<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf"/></rootfiles></container>'''
            opf = '''<package xmlns="http://www.idpf.org/2007/opf"><manifest><item id="cap" href="capitulo.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="cap"/></spine></package>'''
            with zipfile.ZipFile(epub, "w") as pacote:
                pacote.writestr("META-INF/container.xml", container)
                pacote.writestr("OEBPS/content.opf", opf)
                pacote.writestr("OEBPS/capitulo.xhtml", "<html><body><p>Capítulo EPUB</p></body></html>")
            self.assertIn("Capítulo EPUB", ler_documento(epub))


class TestSelecaoNumerica(unittest.TestCase):
    def test_selecao_por_numero_comeca_em_um(self):
        arquivos = [Path("um.txt"), Path("dois.pdf"), Path("tres.epub")]
        self.assertEqual(selecionar_documentos_numericos(arquivos, "2"), [arquivos[1]])
        self.assertEqual(selecionar_documentos_numericos(arquivos, "1,3"), [arquivos[0], arquivos[2]])
        self.assertEqual(selecionar_documentos_numericos(arquivos, "todos"), arquivos)
        with self.assertRaises(ValueError):
            selecionar_documentos_numericos(arquivos, "4")


if __name__ == "__main__":
    unittest.main()
