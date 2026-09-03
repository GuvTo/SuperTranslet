import pandas as pd
import numpy as np
import sklearn as iSk
import statsmodels as iStatsModel
import matplotlib as iMatPlotLib
import scipy as iSciPy
import statsmodels.stats.api as iStatsModel_stats
import statsmodels.formula.formulatools as iStatsModel_formula
import matplotlib.pyplot as iMatPlotLib_PyPlot


def fun_grafico(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):
    """
    Processa as respostas e gera dados para plotagem.

    Args:
        vLetraRepeticao: Lista de letras possíveis
        vTempoLetra: Lista de tempos
        vRespostas: Sequência de respostas
        vOrdemTotal: Dicionário mapeando letra para valor numérico

    Returns:
        Lista com dicionário contendo os dados processados
    """

    fvalor_x_tempo = []
    fvalor_y_repeticao = []
    fvalor_y_intensidadeOuLetra = []
    fOrdemRepeticao = []
    fVolume = []

    # Contador de repetições para cada letra
    contador_repeticao = {}
    for letra in vLetraRepeticao:
        contador_repeticao[letra] = 0

    # Processa cada resposta
    for idx, xResposta in enumerate(vRespostas):
        if xResposta in vLetraRepeticao:
            # Adiciona tempo (índice sequencial)
            fvalor_x_tempo.append(len(fvalor_x_tempo) + 1)

            # Conta repetição da letra
            contador_repeticao[xResposta] += 1

            # Valor de repetição (acumulado por letra)
            fvalor_y_repeticao.append(contador_repeticao[xResposta])

            # Intensidade/letra
            fvalor_y_intensidadeOuLetra.append(xResposta)

            # Ordem da letra (valor numérico do dicionário)
            if xResposta in vOrdemTotal:
                fOrdemRepeticao.append(vOrdemTotal[xResposta])
            else:
                fOrdemRepeticao.append(0)

            # Volume (simulado como 1 por ocorrência)
            fVolume.append(1)

    fvalor_resultado_final = [{
        'vXTempo': fvalor_x_tempo,
        'vYRepeticao': fvalor_y_repeticao,
        'vYLetra': fvalor_y_intensidadeOuLetra,
        'vRepeticao': fOrdemRepeticao,
        'vVolume': fVolume
    }]

    return fvalor_resultado_final


def calcular_macd(dados, periodo_rapido=12, periodo_lento=26, periodo_sinal=9):
    """
    Calcula MACD (Moving Average Convergence Divergence)

    Args:
        dados: Lista de valores
        periodo_rapido: Período da EMA rápida (default 12)
        periodo_lento: Período da EMA lenta (default 26)
        periodo_sinal: Período da linha de sinal (default 9)

    Returns:
        Tuple (macd_line, signal_line, histogram)
    """
    if len(dados) < periodo_lento:
        periodo_lento = len(dados)

    # Calcular EMA
    def ema(dados, periodo):
        if len(dados) < periodo:
            periodo = len(dados)
        k = 2 / (periodo + 1)
        ema_values = [sum(dados[:periodo]) / periodo]
        for i in range(periodo, len(dados)):
            ema_values.append(dados[i] * k + ema_values[-1] * (1 - k))
        return ema_values

    # Calcular EMAs
    ema_rapida = ema(dados, periodo_rapido)
    ema_lenta = ema(dados, periodo_lento)

    # MACD Line = EMA rápida - EMA lenta
    macd_line = []
    for i in range(len(ema_lenta)):
        if i < len(ema_rapida):
            macd_line.append(ema_rapida[i] - ema_lenta[i])
        else:
            macd_line.append(0)

    # Signal Line = EMA do MACD
    signal_line = ema(macd_line, periodo_sinal)

    # Histogram = MACD Line - Signal Line
    histogram = []
    for i in range(len(macd_line)):
        histogram.append(macd_line[i] - signal_line[i] if i < len(signal_line) else 0)

    return macd_line, signal_line, histogram


def fun_final_deck(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):
    """
    Função principal que processa dados e gera gráficos.
    """
    # Processa os dados
    vResux = fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal)

    # Extrai dados processados
    dados = vResux[0]
    vRepeticao = dados['vRepeticao']
    vX = dados['vXTempo']
    vLetras = dados['vYLetra']
    vVolume = dados['vVolume']

    print(f"Dados processados: {len(vRepeticao)} pontos")

    if len(vRepeticao) == 0:
        print("Sem dados para processar!")
        return None

    # Configuração da média móvel
    vCofing = {
        'indicador': {
            'mm': [2, 10, 20],  # Janelas para médias móveis
            'volume': True,
            'macd': {
                'rapido': 12,
                'lento': 26,
                'sinal': 9
            }
        }
    }

    # Cálculo de médias móveis
    fmedia_movel_curta = []
    fmedia_movel_media = []
    fmedia_movel_longa = []
    fmedia_movel_todas = {}

    for i in range(len(vRepeticao)):
        # Média móvel curta (janela 2)
        if i >= vCofing['indicador']['mm'][0] - 1:
            janela_curta = vRepeticao[i - vCofing['indicador']['mm'][0] + 1: i + 1]
            fmedia_movel_curta.append(sum(janela_curta) / len(janela_curta))
        else:
            fmedia_movel_curta.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

        # Média móvel média (janela 10)
        if i >= vCofing['indicador']['mm'][1] - 1:
            janela_media = vRepeticao[i - vCofing['indicador']['mm'][1] + 1: i + 1]
            fmedia_movel_media.append(sum(janela_media) / len(janela_media))
        else:
            fmedia_movel_media.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

        # Média móvel longa (janela 20)
        if i >= vCofing['indicador']['mm'][2] - 1:
            janela_longa = vRepeticao[i - vCofing['indicador']['mm'][2] + 1: i + 1]
            fmedia_movel_longa.append(sum(janela_longa) / len(janela_longa))
        else:
            fmedia_movel_longa.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

    # Normalização para probabilidade (0-1)
    fprobabilidade_deox_curta = []
    fprobabilidade_deox_media = []
    fprobabilidade_deox_longa = []

    max_valor = max(vRepeticao) if vRepeticao else 1

    for i in range(len(fmedia_movel_curta)):
        if max_valor > 0:
            fprobabilidade_deox_curta.append(fmedia_movel_curta[i] / max_valor)
            fprobabilidade_deox_media.append(fmedia_movel_media[i] / max_valor)
            fprobabilidade_deox_longa.append(fmedia_movel_longa[i] / max_valor)
        else:
            fprobabilidade_deox_curta.append(0)
            fprobabilidade_deox_media.append(0)
            fprobabilidade_deox_longa.append(0)

    # Calcular MACD
    macd_line, signal_line, histogram = calcular_macd(
        vRepeticao,
        vCofing['indicador']['macd']['rapido'],
        vCofing['indicador']['macd']['lento'],
        vCofing['indicador']['macd']['sinal']
    )

    # Criar figura com 6 subplots
    fig = iMatPlotLib_PyPlot.figure(figsize=(14, 16))

    # Gráfico 1: Repetições e médias móveis
    ax1 = fig.add_subplot(6, 1, 1)
    ax1.plot(vX, vRepeticao, 'b-', label='Repetição da Letra', linewidth=2)
    ax1.plot(vX, fmedia_movel_curta, 'r--', label=f"MM Curta ({vCofing['indicador']['mm'][0]})", linewidth=2)
    ax1.plot(vX, fmedia_movel_media, 'g--', label=f"MM Média ({vCofing['indicador']['mm'][1]})", linewidth=2)
    ax1.plot(vX, fmedia_movel_longa, 'y--', label=f"MM Longa ({vCofing['indicador']['mm'][2]})", linewidth=2)

    ax1.set_xlabel('Tempo/Índice')
    ax1.set_ylabel('Valor de Repetição')
    ax1.set_title('Análise de Repetições de Letras com Médias Móveis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Probabilidades normalizadas
    ax2 = fig.add_subplot(6, 1, 2)
    ax2.plot(vX, fprobabilidade_deox_curta, 'r-', label='Probabilidade MM Curta', linewidth=2)
    ax2.plot(vX, fprobabilidade_deox_media, 'g-', label='Probabilidade MM Média', linewidth=2)
    ax2.plot(vX, fprobabilidade_deox_longa, 'y-', label='Probabilidade MM Longa', linewidth=2)

    ax2.set_xlabel('Tempo/Índice')
    ax2.set_ylabel('Probabilidade Normalizada')
    ax2.set_title('Probabilidades Normalizadas das Médias Móveis')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Gráfico 3: Letras representadas por números (1-7)
    ax3 = fig.add_subplot(6, 1, 3)

    # Cores para cada número (1-7)
    cores = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    labels_numeros = ['1', '2', '3', '4', '5', '6', '7']

    # Plotar cada letra como ponto com seu número correspondente
    for i in range(len(vX)):
        numero = vRepeticao[i]  # Número da letra (1-7)
        letra = vLetras[i]

        # Escolher cor baseada no número
        cor_idx = min(numero - 1, len(cores) - 1) if numero > 0 else 0
        cor = cores[cor_idx]

        # Plotar ponto
        ax3.scatter(vX[i], numero, c=cor, s=50, alpha=0.7)

        # Adicionar texto com a letra
        ax3.annotate(letra, (vX[i], numero),
                     textcoords="offset points",
                     xytext=(5, 5),
                     fontsize=8,
                     color='black')

    # Configurar eixo Y para mostrar números de 1 a 7
    ax3.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax3.set_yticklabels(labels_numeros)

    # Adicionar linha de tendência
    if len(vX) > 1:
        z = np.polyfit(vX, vRepeticao, 1)  # Regressão linear
        p = np.poly1d(z)
        ax3.plot(vX, p(vX), "k--", alpha=0.5, label='Tendência Linear')

    ax3.set_xlabel('Tempo/Índice')
    ax3.set_ylabel('Número da Letra (1-7)')
    ax3.set_title('Letras Representadas por Números (1-7)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # Adicionar legenda explicativa
    legenda_texto = "Legenda:\n"
    for num in range(1, 8):
        letras_com_numero = [letra for letra, valor in vOrdemTotal.items() if valor == num]
        if letras_com_numero:
            legenda_texto += f"{num}: {', '.join(letras_com_numero)}\n"

    # Adicionar caixa de texto com legenda
    ax3.text(0.02, 0.98, legenda_texto, transform=ax3.transAxes,
             fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Gráfico 4: Volume
    ax4 = fig.add_subplot(6, 1, 4)

    # Barras de volume
    cores_volume = []
    for i in range(len(vVolume)):
        if i < len(vRepeticao) and vRepeticao[i] > (fmedia_movel_curta[i] if i < len(fmedia_movel_curta) else 0):
            cores_volume.append('green')  # Volume positivo
        else:
            cores_volume.append('red')  # Volume negativo

    ax4.bar(vX, vVolume, color=cores_volume, alpha=0.7, label='Volume')
    ax4.set_xlabel('Tempo/Índice')
    ax4.set_ylabel('Volume')
    ax4.set_title('Volume de Ocorrências')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # Gráfico 5: MACD
    ax5 = fig.add_subplot(6, 1, 5)

    # MACD Line
    ax5.plot(vX, macd_line, 'b-',
             label=f'MACD Line ({vCofing["indicador"]["macd"]["rapido"]}/{vCofing["indicador"]["macd"]["lento"]})',
             linewidth=2)

    # Signal Line
    ax5.plot(vX, signal_line, 'r-', label=f'Signal Line ({vCofing["indicador"]["macd"]["sinal"]})', linewidth=2)

    # Zero line
    ax5.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    ax5.set_xlabel('Tempo/Índice')
    ax5.set_ylabel('MACD')
    ax5.set_title('MACD (Moving Average Convergence Divergence)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # Gráfico 6: MACD Histograma
    ax6 = fig.add_subplot(6, 1, 6)

    # Histograma com cores
    cores_hist = ['green' if val >= 0 else 'red' for val in histogram]
    ax6.bar(vX, histogram, color=cores_hist, alpha=0.7, label='MACD Histograma')

    # Zero line
    ax6.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    ax6.set_xlabel('Tempo/Índice')
    ax6.set_ylabel('Histograma')
    ax6.set_title('MACD Histograma')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    iMatPlotLib_PyPlot.tight_layout()

    #
    iMatPlotLib.pyplot.savefig(f'adex_file_imagem_erx{str(np.random.randint(0, 1000000000))}edx_id{str(np.random.randint(0, 1000000))}')
    #


    iMatPlotLib_PyPlot.show()

    # Retorna resultados para análise posterior
    return {
        'dados_processados': dados,
        'media_movel_curta': fmedia_movel_curta,
        'media_movel_media': fmedia_movel_media,
        'media_movel_longa': fmedia_movel_longa,
        'probabilidade_curta': fprobabilidade_deox_curta,
        'probabilidade_media': fprobabilidade_deox_media,
        'probabilidade_longa': fprobabilidade_deox_longa,
        'volume': vVolume,
        'macd_line': macd_line,
        'signal_line': signal_line,
        'histogram': histogram
    }


# Dados de teste corrigidos
vFrinxn = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r'],  # Letras possíveis
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],  # Tempos
    ['a', 'd', 'e', 'a', 'b', 'c', 'a', 'd', 'e', 'f', 'a', 'b', 'g', 'h', 'i', 'j'],  # Respostas
    {
        'a': 1, 'b': 1, 'c': 2, 'd': 2, 'e': 2, 'f': 3, 'g': 3,
        'h': 4, 'i': 4, 'j': 4, 'k': 5, 'm': 5, 'n': 6, 'o': 6,
        'p': 6, 'q': 7, 'r': 7
    }  # Ordem total
]

if __name__ == '__main__':
    print("Iniciando análise completa...")
    print("Indicadores incluídos:")
    print("1. Médias Móveis (2, 10, 20)")
    print("2. Probabilidades Normalizadas")
    print("3. Letras Representadas por Números (1-7)")
    print("4. Volume")
    print("5. MACD")
    print("6. MACD Histograma")
    print("=" * 50)

    resultado = fun_final_deck(vFrinxn[0], vFrinxn[1], vFrinxn[2], vFrinxn[3])

    if resultado:
        print("\n=== Resultados da Análise ===")
        print(f"Número de pontos processados: {len(resultado['dados_processados']['vXTempo'])}")
        print(f"Média móvel curta (último valor): {resultado['media_movel_curta'][-1]:.3f}")
        print(f"Média móvel média (último valor): {resultado['media_movel_media'][-1]:.3f}")
        print(f"Média móvel longa (último valor): {resultado['media_movel_longa'][-1]:.3f}")
        print(f"Probabilidade curta (último valor): {resultado['probabilidade_curta'][-1]:.3f}")
        print(f"Probabilidade média (último valor): {resultado['probabilidade_media'][-1]:.3f}")
        print(f"Probabilidade longa (último valor): {resultado['probabilidade_longa'][-1]:.3f}")
        print(f"Volume total: {sum(resultado['volume'])}")
        print(f"MACD Line (último valor): {resultado['macd_line'][-1]:.3f}")
        print(f"Signal Line (último valor): {resultado['signal_line'][-1]:.3f}")
        print(f"Histograma (último valor): {resultado['histogram'][-1]:.3f}")

        # Análise MACD
        if resultado['histogram'][-1] > 0:
            print("Sinal MACD: POSITIVO (tendência de alta)")
        else:
            print("Sinal MACD: NEGATIVO (tendência de baixa)")