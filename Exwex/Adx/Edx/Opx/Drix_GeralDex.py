import pandas as pd
import numpy as np
import sklearn as iSk
import statsmodels as iStatsModel
import matplotlib as iMatPlotLib
import scipy as iSciPy
import statsmodels.stats.api as iStatsModel_stats
import statsmodels.formula.formulatools as iStatsModel_formula
import matplotlib.pyplot as iMatPlotLib_PyPlot
import argparse
import os
import sys
import json
import random
import string
import signal
from datetime import datetime

# ================== TRADUÇÕES ==================
IDIOMAS = {
    'pt': {
        'bem_vindo': "Bem-vindo ao analisador de letras!",
        'idioma': "Idioma selecionado: Português",
        'letras': "Digite as letras separadas por espaço (ex: a b c): ",
        'tempos': "Digite os tempos separados por espaço (ex: 1 2 3): ",
        'respostas': "Digite as respostas separadas por espaço (ex: a b a c): ",
        'ordem': "Digite a ordem (ex: a=1 b=2 c=3): ",
        'dir_save': "Diretório para salvar (Enter para padrão): ",
        'nome_arquivo': "Nome do arquivo (Enter para aleatório): ",
        'salvando': "Salvando resultados...",
        'sucesso': "Arquivos salvos com sucesso!",
        'erro': "Erro: {0}",
        'saindo': "Encerrando..."
    },
    'en': {
        'bem_vindo': "Welcome to the letter analyzer!",
        'idioma': "Selected language: English",
        'letras': "Enter letters separated by space (e.g., a b c): ",
        'tempos': "Enter times separated by space (e.g., 1 2 3): ",
        'respostas': "Enter answers separated by space (e.g., a b a c): ",
        'ordem': "Enter order (e.g., a=1 b=2 c=3): ",
        'dir_save': "Directory to save (Enter for default): ",
        'nome_arquivo': "File name (Enter for random): ",
        'salvando': "Saving results...",
        'sucesso': "Files saved successfully!",
        'erro': "Error: {0}",
        'saindo': "Exiting..."
    },
    'fr': {
        'bem_vindo': "Bienvenue à l'analyseur de lettres !",
        'idioma': "Langue sélectionnée : Français",
        'letras': "Entrez les lettres séparées par un espace (ex : a b c) : ",
        'tempos': "Entrez les temps séparés par un espace (ex : 1 2 3) : ",
        'respostas': "Entrez les réponses séparées par un espace (ex : a b a c) : ",
        'ordem': "Entrez l'ordre (ex : a=1 b=2 c=3) : ",
        'dir_save': "Répertoire de sauvegarde (Entrée pour défaut) : ",
        'nome_arquivo': "Nom du fichier (Entrée pour aléatoire) : ",
        'salvando': "Enregistrement des résultats...",
        'sucesso': "Fichiers enregistrés avec succès !",
        'erro': "Erreur : {0}",
        'saindo': "Fermeture..."
    },
    'es': {
        'bem_vindo': "¡Bienvenido al analizador de letras!",
        'idioma': "Idioma seleccionado: Español",
        'letras': "Ingrese las letras separadas por espacio (ej: a b c): ",
        'tempos': "Ingrese los tiempos separados por espacio (ej: 1 2 3): ",
        'respostas': "Ingrese las respuestas separadas por espacio (ej: a b a c): ",
        'ordem': "Ingrese el orden (ej: a=1 b=2 c=3): ",
        'dir_save': "Directorio para guardar (Enter para predeterminado): ",
        'nome_arquivo': "Nombre del archivo (Enter para aleatorio): ",
        'salvando': "Guardando resultados...",
        'sucesso': "Archivos guardados con éxito!",
        'erro': "Error: {0}",
        'saindo': "Saliendo..."
    },
    'ar': {
        'bem_vindo': "مرحباً بك في محلل الحروف!",
        'idioma': "اللغة المختارة: العربية",
        'letras': "أدخل الحروف مفصولة بمسافة (مثال: أ ب ج): ",
        'tempos': "أدخل الأوقات مفصولة بمسافة (مثال: 1 2 3): ",
        'respostas': "أدخل الإجابات مفصولة بمسافة (مثال: أ ب أ ج): ",
        'ordem': "أدخل الترتيب (مثال: أ=1 ب=2 ج=3): ",
        'dir_save': "دليل الحفظ (اضغط Enter للافتراضي): ",
        'nome_arquivo': "اسم الملف (اضغط Enter لعشوائي): ",
        'salvando': "جاري حفظ النتائج...",
        'sucesso': "تم حفظ الملفات بنجاح!",
        'erro': "خطأ: {0}",
        'saindo': "جارٍ الخروج..."
    },
    'it': {
        'bem_vindo': "Benvenuto nell'analizzatore di lettere!",
        'idioma': "Lingua selezionata: Italiano",
        'letras': "Inserisci le lettere separate da spazio (es: a b c): ",
        'tempos': "Inserisci i tempi separati da spazio (es: 1 2 3): ",
        'respostas': "Inserisci le risposte separate da spazio (es: a b a c): ",
        'ordem': "Inserisci l'ordine (es: a=1 b=2 c=3): ",
        'dir_save': "Directory per salvare (Invio per predefinita): ",
        'nome_arquivo': "Nome del file (Invio per casuale): ",
        'salvando': "Salvataggio dei risultati...",
        'sucesso': "File salvati con successo!",
        'erro': "Errore: {0}",
        'saindo': "Uscita..."
    }
}


# ================== FUNÇÕES AUXILIARES ==================
def calcular_ema(dados, periodo):
    if len(dados) == 0:
        return []
    ema = [dados[0]]
    multiplicador = 2 / (periodo + 1)
    for i in range(1, len(dados)):
        ema.append((dados[i] - ema[i - 1]) * multiplicador + ema[i - 1])
    return ema


def calcular_macd(dados, rapido=12, lento=26, sinal=9):
    if len(dados) == 0:
        return [], [], []
    ema_rapida = calcular_ema(dados, rapido)
    ema_lenta = calcular_ema(dados, lento)
    macd_line = [r - l for r, l in zip(ema_rapida, ema_lenta)]
    signal_line = calcular_ema(macd_line, sinal)
    hist = [m - s for m, s in zip(macd_line, signal_line)]
    return macd_line, signal_line, hist


def gerar_nome_aleatorio(ext=".png"):
    """Gera um nome de arquivo aleatório."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ext


def salvar_estado(dados, caminho):
    """Salva dados em JSON (robusto)."""
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar estado: {e}")


def salvar_grafico(fig, caminho):
    """Salva a figura em arquivo."""
    try:
        fig.savefig(caminho, dpi=150, bbox_inches='tight')
    except Exception as e:
        print(f"Erro ao salvar gráfico: {e}")


# ================== FUNÇÃO ORIGINAL (Adaptada) ==================
def fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal):
    fvalor_x_tempo = []
    fvalor_y_repeticao = []
    fvalor_y_intensidadeOuLetra = []
    fOrdemRepeticao = []

    contador_repeticao = {letra: 0 for letra in vLetraRepeticao}
    for xResposta in vRespostas:
        if xResposta in vLetraRepeticao:
            fvalor_x_tempo.append(len(fvalor_x_tempo) + 1)
            contador_repeticao[xResposta] += 1
            fvalor_y_repeticao.append(contador_repeticao[xResposta])
            fvalor_y_intensidadeOuLetra.append(xResposta)
            if xResposta in vOrdemTotal:
                fOrdemRepeticao.append(vOrdemTotal[xResposta])
            else:
                fOrdemRepeticao.append(0)

    return [{
        'vXTempo': fvalor_x_tempo,
        'vYRepeticao': fvalor_y_repeticao,
        'vYLetra': fvalor_y_intensidadeOuLetra,
        'vRepeticao': fOrdemRepeticao
    }]


def fun_final_deck(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal):
    vResux = fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal)
    dados = vResux[0]
    vRepeticao = dados['vRepeticao']
    vX = dados['vXTempo']
    vLetras = dados['vYLetra']

    if len(vRepeticao) == 0:
        return None, None

    # Médias Móveis
    vCofing = {'indicador': {'mm': [2, 10]}}
    fmedia_movel_curta, fmedia_movel_longa = [], []
    for i in range(len(vRepeticao)):
        if i >= vCofing['indicador']['mm'][0] - 1:
            janela = vRepeticao[i - vCofing['indicador']['mm'][0] + 1: i + 1]
            fmedia_movel_curta.append(sum(janela) / len(janela))
        else:
            fmedia_movel_curta.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

        if i >= vCofing['indicador']['mm'][1] - 1:
            janela = vRepeticao[i - vCofing['indicador']['mm'][1] + 1: i + 1]
            fmedia_movel_longa.append(sum(janela) / len(janela))
        else:
            fmedia_movel_longa.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

    # Probabilidades
    max_valor = max(vRepeticao) if vRepeticao else 1
    fprobabilidade_curta = [m / max_valor for m in fmedia_movel_curta]
    fprobabilidade_longa = [m / max_valor for m in fmedia_movel_longa]

    # Volume
    volume = [0]
    for i in range(1, len(vRepeticao)):
        volume.append(abs(vRepeticao[i] - vRepeticao[i - 1]))

    # MACD
    macd_line, signal_line, hist_macd = calcular_macd(vRepeticao)

    # Gráficos
    fig = iMatPlotLib_PyPlot.figure(figsize=(14, 14))

    # Subplot 1: Repetições e MMs
    ax1 = fig.add_subplot(5, 1, 1)
    ax1.plot(vX, vRepeticao, 'b-', label='Valor da Letra (1-7)', linewidth=2)
    ax1.plot(vX, fmedia_movel_curta, 'r--', label='MM Curta (2)', linewidth=2)
    ax1.plot(vX, fmedia_movel_longa, 'g--', label='MM Longa (10)', linewidth=2)
    ax1.set_title('Repetições e Médias Móveis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Probabilidades
    ax2 = fig.add_subplot(5, 1, 2)
    ax2.plot(vX, fprobabilidade_curta, 'r-', label='Prob. MM Curta')
    ax2.plot(vX, fprobabilidade_longa, 'g-', label='Prob. MM Longa')
    ax2.set_title('Probabilidades Normalizadas')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Subplot 3: Letras → números
    ax3 = fig.add_subplot(5, 1, 3)
    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    labels_numeros = ['1', '2', '3', '4', '5', '6', '7']
    for i in range(len(vX)):
        numero = vRepeticao[i]
        letra = vLetras[i]
        cor_idx = min(numero - 1, 6) if numero > 0 else 0
        ax3.scatter(vX[i], numero, c=cores[cor_idx], s=50, alpha=0.7)
        ax3.annotate(letra, (vX[i], numero), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax3.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax3.set_yticklabels(labels_numeros)
    if len(vX) > 1:
        z = np.polyfit(vX, vRepeticao, 1)
        p = np.poly1d(z)
        ax3.plot(vX, p(vX), "k--", alpha=0.5, label='Tendência Linear')
    ax3.set_title('Letras Representadas por Números (1-7)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Subplot 4: Volume
    ax4 = fig.add_subplot(5, 1, 4)
    ax4.bar(vX, volume, color='steelblue', alpha=0.7, label='Volume')
    ax4.set_title('Volume (variação absoluta)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Subplot 5: MACD
    ax5 = fig.add_subplot(5, 1, 5)
    ax5.plot(vX, macd_line, 'b-', label='MACD (12,26)', linewidth=2)
    ax5.plot(vX, signal_line, 'r-', label='Sinal (9)', linewidth=2)
    cores_hist = ['green' if h >= 0 else 'red' for h in hist_macd]
    ax5.bar(vX, hist_macd, color=cores_hist, alpha=0.5, label='Histograma')
    ax5.axhline(0, color='black', linewidth=0.8)
    ax5.set_title('MACD com Histograma')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    iMatPlotLib_PyPlot.tight_layout()

    # Retorna dados, figura e resultados
    resultados = {
        'dados': dados,
        'media_movel_curta': fmedia_movel_curta,
        'media_movel_longa': fmedia_movel_longa,
        'probabilidade_curta': fprobabilidade_curta,
        'probabilidade_longa': fprobabilidade_longa,
        'volume': volume,
        'macd_line': macd_line,
        'signal_line': signal_line,
        'hist_macd': hist_macd
    }
    return fig, resultados


# ================== INTERFACE CLI ==================
def parse_args():
    parser = argparse.ArgumentParser(description="Analisador de letras com indicadores técnicos.")
    parser.add_argument('--idioma', '-i', choices=['pt', 'en', 'fr', 'es', 'ar', 'it'], default='pt',
                        help='Idioma do programa (padrão: pt)')
    parser.add_argument('--letras', '-l', nargs='+',
                        default=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r'],
                        help='Lista de letras possíveis')
    parser.add_argument('--tempos', '-t', nargs='+', type=int, default=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        help='Tempos (índices)')
    parser.add_argument('--respostas', '-r', nargs='+',
                        default=['a', 'd', 'e', 'a', 'b', 'c', 'a', 'd', 'e', 'f', 'a', 'b', 'g', 'h', 'i', 'j'],
                        help='Sequência de respostas')
    parser.add_argument('--ordem', '-o', nargs='+',
                        default=['a=1', 'b=1', 'c=2', 'd=2', 'e=2', 'f=3', 'g=3', 'h=4', 'i=4', 'j=4', 'k=5', 'm=5',
                                 'n=6', 'o=6', 'p=6', 'q=7', 'r=7'],
                        help='Ordem das letras (ex: a=1 b=2)')
    parser.add_argument('--dir', '-d', default='', help='Diretório para salvar (vazio = padrão)')
    parser.add_argument('--nome', '-n', default='', help='Nome do arquivo (vazio = aleatório)')
    parser.add_argument('--interativo', action='store_true', help='Modo interativo (perguntas)')
    return parser.parse_args()


def processar_ordem(lista_ordem):
    d = {}
    for item in lista_ordem:
        if '=' in item:
            chave, valor = item.split('=')
            d[chave] = int(valor)
    return d


def main():
    args = parse_args()
    idioma = args.idioma
    textos = IDIOMAS[idioma]

    print(textos['bem_vindo'])
    print(textos['idioma'])

    # Se modo interativo, solicitar dados
    if args.interativo:
        letras = input(textos['letras']).strip().split()
        tempos = list(map(int, input(textos['tempos']).strip().split()))
        respostas = input(textos['respostas']).strip().split()
        ordem_input = input(textos['ordem']).strip().split()
        ordem = processar_ordem(ordem_input)
        dir_save = input(textos['dir_save']).strip()
        nome_arquivo = input(textos['nome_arquivo']).strip()
    else:
        letras = args.letras
        tempos = args.tempos
        respostas = args.respostas
        ordem = processar_ordem(args.ordem)
        dir_save = args.dir
        nome_arquivo = args.nome

    # Diretório padrão
    if not dir_save:
        dir_save = os.getcwd()
    if not os.path.exists(dir_save):
        os.makedirs(dir_save, exist_ok=True)

    # Nome do arquivo
    if not nome_arquivo:
        nome_arquivo = gerar_nome_aleatorio(".png")
    elif not nome_arquivo.endswith(".png"):
        nome_arquivo += ".png"

    caminho_img = os.path.join(dir_save, nome_arquivo)
    caminho_dados = os.path.join(dir_save, nome_arquivo.replace(".png", ".json"))

    # Processar análise
    print(textos['salvando'])
    try:
        fig, resultados = fun_final_deck(letras, tempos, respostas, ordem)
        if fig is None:
            print(textos['erro'].format("Sem dados para processar"))
            sys.exit(1)

        # Salvar gráfico
        salvar_grafico(fig, caminho_img)

        # Salvar dados (incluindo inputs) em JSON
        dados_salvar = {
            'timestamp': datetime.now().isoformat(),
            'idioma': idioma,
            'letras': letras,
            'tempos': tempos,
            'respostas': respostas,
            'ordem': ordem,
            'resultados': resultados
        }
        salvar_estado(dados_salvar, caminho_dados)

        print(textos['sucesso'])
        print(f"Imagem: {caminho_img}")
        print(f"Dados: {caminho_dados}")

    except Exception as e:
        print(textos['erro'].format(str(e)))
        # Salvar estado mesmo com erro (se possível)
        try:
            erro_dados = {
                'timestamp': datetime.now().isoformat(),
                'erro': str(e),
                'inputs': {'letras': letras, 'tempos': tempos, 'respostas': respostas, 'ordem': ordem}
            }
            caminho_erro = os.path.join(dir_save, "erro_" + gerar_nome_aleatorio(".json"))
            salvar_estado(erro_dados, caminho_erro)
        except:
            pass
        sys.exit(1)


# ================== HANDLER DE SINAL (salva em SIGINT) ==================
def signal_handler(sig, frame):
    print("\nInterrupção detectada. Tentando salvar...")
    # Salvar estado atual (se houver variáveis em escopo) - aqui uma implementação simples
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()