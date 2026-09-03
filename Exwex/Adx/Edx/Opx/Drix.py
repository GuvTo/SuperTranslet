import pandas as pd
import numpy as np
import sklearn as iSk
import statsmodels as iStatsModel
import matplotlib as iMatPlotLib
import scipy as iSciPy
import statsmodels.stats.api as iStatsModel_stats
import statsmodels.formula.formulatools as iStatsModel_formula
import matplotlib.pyplot as iMatPlotLib_PyPlot


# ================== Função de EMA (Exponential Moving Average) ==================
def calcular_ema(dados, periodo):
    """Calcula a Média Móvel Exponencial de uma série."""
    ema = [dados[0]]  # primeiro valor é o próprio dado
    multiplicador = 2 / (periodo + 1)
    for i in range(1, len(dados)):
        ema.append((dados[i] - ema[i - 1]) * multiplicador + ema[i - 1])
    return ema


# ================== Função de MACD ==================
def calcular_macd(dados, periodo_rapido=12, periodo_lento=26, periodo_sinal=9):
    """Calcula MACD, linha de sinal e histograma."""
    # EMA rápida e lenta
    ema_rapida = calcular_ema(dados, periodo_rapido)
    ema_lenta = calcular_ema(dados, periodo_lento)

    # MACD line = EMA rápida - EMA lenta
    macd_line = [rapida - lenta for rapida, lenta in zip(ema_rapida, ema_lenta)]

    # Signal line = EMA do MACD
    signal_line = calcular_ema(macd_line, periodo_sinal)

    # Histogram = MACD - Signal
    histogram = [macd - sinal for macd, sinal in zip(macd_line, signal_line)]

    return macd_line, signal_line, histogram


# ================== Função gráfico original (mantida) ==================
def fun_grafico(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):
    """
    Processa as respostas e gera dados para plotagem.
    """
    fvalor_x_tempo = []
    fvalor_y_repeticao = []
    fvalor_y_intensidadeOuLetra = []
    fOrdemRepeticao = []

    # Contador de repetições para cada letra
    contador_repeticao = {}
    for letra in vLetraRepeticao:
        contador_repeticao[letra] = 0

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

    fvalor_resultado_final = [{
        'vXTempo': fvalor_x_tempo,
        'vYRepeticao': fvalor_y_repeticao,
        'vYLetra': fvalor_y_intensidadeOuLetra,
        'vRepeticao': fOrdemRepeticao
    }]

    return fvalor_resultado_final


# ================== Função principal com todos os indicadores ==================
def fun_final_deck(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):
    """
    Processa dados, calcula médias móveis, volume, MACD e gera gráficos.
    """
    # Processa os dados
    vResux = fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal)
    dados = vResux[0]
    vRepeticao = dados['vRepeticao']  # valores numéricos (1-7)
    vX = dados['vXTempo']
    vLetras = dados['vYLetra']

    print(f"Dados processados: {len(vRepeticao)} pontos")

    if len(vRepeticao) == 0:
        print("Sem dados para processar!")
        return None

    # ---------- Médias Móveis (já existiam) ----------
    vCofing = {'indicador': {'mm': [2, 10]}}

    fmedia_movel_curta = []
    fmedia_movel_longa = []

    for i in range(len(vRepeticao)):
        if i >= vCofing['indicador']['mm'][0] - 1:
            janela_curta = vRepeticao[i - vCofing['indicador']['mm'][0] + 1: i + 1]
            fmedia_movel_curta.append(sum(janela_curta) / len(janela_curta))
        else:
            fmedia_movel_curta.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

        if i >= vCofing['indicador']['mm'][1] - 1:
            janela_longa = vRepeticao[i - vCofing['indicador']['mm'][1] + 1: i + 1]
            fmedia_movel_longa.append(sum(janela_longa) / len(janela_longa))
        else:
            fmedia_movel_longa.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

    # ---------- Probabilidades Normalizadas (já existiam) ----------
    max_valor = max(vRepeticao) if vRepeticao else 1
    fprobabilidade_deox_curta = [m / max_valor for m in fmedia_movel_curta]
    fprobabilidade_deox_longa = [m / max_valor for m in fmedia_movel_longa]

    # ---------- Volume (novo) ----------
    # Definimos volume como a variação absoluta entre valores consecutivos
    volume = [0]  # primeiro ponto sem variação
    for i in range(1, len(vRepeticao)):
        volume.append(abs(vRepeticao[i] - vRepeticao[i - 1]))

    # ---------- MACD (novo) ----------
    macd_line, signal_line, hist_macd = calcular_macd(vRepeticao, 12, 26, 9)

    # ---------- Gráficos ----------
    fig = iMatPlotLib_PyPlot.figure(figsize=(14, 14))

    # Subplot 1: Repetições e Médias Móveis
    ax1 = fig.add_subplot(5, 1, 1)
    ax1.plot(vX, vRepeticao, 'b-', label='Valor da Letra (1-7)', linewidth=2)
    ax1.plot(vX, fmedia_movel_curta, 'r--', label=f"MM Curta ({vCofing['indicador']['mm'][0]})", linewidth=2)
    ax1.plot(vX, fmedia_movel_longa, 'g--', label=f"MM Longa ({vCofing['indicador']['mm'][1]})", linewidth=2)
    ax1.set_xlabel('Tempo/Índice')
    ax1.set_ylabel('Valor de Repetição')
    ax1.set_title('1. Repetições e Médias Móveis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Subplot 2: Probabilidades Normalizadas
    ax2 = fig.add_subplot(5, 1, 2)
    ax2.plot(vX, fprobabilidade_deox_curta, 'r-', label='Prob. MM Curta', linewidth=2)
    ax2.plot(vX, fprobabilidade_deox_longa, 'g-', label='Prob. MM Longa', linewidth=2)
    ax2.set_xlabel('Tempo/Índice')
    ax2.set_ylabel('Probabilidade Normalizada')
    ax2.set_title('2. Probabilidades Normalizadas')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Subplot 3: Letras representadas por números (1-7)
    ax3 = fig.add_subplot(5, 1, 3)
    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    labels_numeros = ['1', '2', '3', '4', '5', '6', '7']

    for i in range(len(vX)):
        numero = vRepeticao[i]
        letra = vLetras[i]
        cor_idx = min(numero - 1, len(cores) - 1) if numero > 0 else 0
        cor = cores[cor_idx]
        ax3.scatter(vX[i], numero, c=cor, s=50, alpha=0.7)
        ax3.annotate(letra, (vX[i], numero), textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax3.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax3.set_yticklabels(labels_numeros)
    if len(vX) > 1:
        z = np.polyfit(vX, vRepeticao, 1)
        p = np.poly1d(z)
        ax3.plot(vX, p(vX), "k--", alpha=0.5, label='Tendência Linear')
    ax3.set_xlabel('Tempo/Índice')
    ax3.set_ylabel('Número da Letra (1-7)')
    ax3.set_title('3. Letras Representadas por Números (1-7)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Legenda da letra→número
    legenda_texto = "Legenda:\n"
    for num in range(1, 8):
        letras_com_numero = [letra for letra, valor in vOrdemTotal.items() if valor == num]
        if letras_com_numero:
            legenda_texto += f"{num}: {', '.join(letras_com_numero)}\n"
    ax3.text(0.02, 0.98, legenda_texto, transform=ax3.transAxes,
             fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Subplot 4: Volume
    ax4 = fig.add_subplot(5, 1, 4)
    ax4.bar(vX, volume, color='steelblue', alpha=0.7, label='Volume (variação absoluta)')
    ax4.set_xlabel('Tempo/Índice')
    ax4.set_ylabel('Volume')
    ax4.set_title('4. Volume (Variação Absoluta entre Valores)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Subplot 5: MACD com Histograma
    ax5 = fig.add_subplot(5, 1, 5)
    # Linha MACD
    ax5.plot(vX, macd_line, 'b-', label='MACD (12,26)', linewidth=2)
    # Linha de Sinal
    ax5.plot(vX, signal_line, 'r-', label='Sinal (9)', linewidth=2)
    # Histograma (barras coloridas conforme positivo/negativo)
    cores_hist = ['green' if h >= 0 else 'red' for h in hist_macd]
    ax5.bar(vX, hist_macd, color=cores_hist, alpha=0.5, label='Histograma')
    ax5.axhline(0, color='black', linewidth=0.8)
    ax5.set_xlabel('Tempo/Índice')
    ax5.set_ylabel('MACD')
    ax5.set_title('5. MACD com Histograma')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    iMatPlotLib_PyPlot.tight_layout()
    iMatPlotLib_PyPlot.show()

    # Retorna resultados
    return {
        'dados_processados': dados,
        'media_movel_curta': fmedia_movel_curta,
        'media_movel_longa': fmedia_movel_longa,
        'probabilidade_curta': fprobabilidade_deox_curta,
        'probabilidade_longa': fprobabilidade_deox_longa,
        'volume': volume,
        'macd_line': macd_line,
        'signal_line': signal_line,
        'hist_macd': hist_macd
    }


# ================== Dados de Teste ==================
vFrinxn = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r'],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    ['a', 'd', 'e', 'a', 'b', 'c', 'a', 'd', 'e', 'f', 'a', 'b', 'g', 'h', 'i', 'j'],
    {
        'a': 1, 'b': 1, 'c': 2, 'd': 2, 'e': 2, 'f': 3, 'g': 3,
        'h': 4, 'i': 4, 'j': 4, 'k': 5, 'm': 5, 'n': 6, 'o': 6,
        'p': 6, 'q': 7, 'r': 7
    }
]

if __name__ == '__main__':
    print("Iniciando análise completa...")
    resultado = fun_final_deck(vFrinxn[0], vFrinxn[1], vFrinxn[2], vFrinxn[3])

    if resultado:
        print("\n=== Resultados da Análise ===")
        print(f"Número de pontos processados: {len(resultado['dados_processados']['vXTempo'])}")
        print(f"Média móvel curta (último valor): {resultado['media_movel_curta'][-1]:.3f}")
        print(f"Média móvel longa (último valor): {resultado['media_movel_longa'][-1]:.3f}")
        print(f"Probabilidade curta (último valor): {resultado['probabilidade_curta'][-1]:.3f}")
        print(f"Probabilidade longa (último valor): {resultado['probabilidade_longa'][-1]:.3f}")
        print(f"Volume total: {sum(resultado['volume'])}")
        print(f"MACD (último valor): {resultado['macd_line'][-1]:.3f}")
        print(f"Sinal (último valor): {resultado['signal_line'][-1]:.3f}")
        print(f"Histograma MACD (último valor): {resultado['hist_macd'][-1]:.3f}")