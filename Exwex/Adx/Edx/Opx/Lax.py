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

    # Contador de repetições para cada letra
    contador_repeticao = {}
    for letra in vLetraRepeticao:
        contador_repeticao[letra] = 0

    # Processa cada resposta
    for xResposta in vRespostas:
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

    fvalor_resultado_final = [{
        'vXTempo': fvalor_x_tempo,
        'vYRepeticao': fvalor_y_repeticao,
        'vYLetra': fvalor_y_intensidadeOuLetra,
        'vRepeticao': fOrdemRepeticao
    }]

    return fvalor_resultado_final


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

    print(f"Dados processados: {len(vRepeticao)} pontos")

    if len(vRepeticao) == 0:
        print("Sem dados para processar!")
        return None

    # Configuração da média móvel
    vCofing = {
        'indicador': {
            'mm': [2, 10]  # Janelas para médias móveis
        }
    }

    # Cálculo de médias móveis
    fmedia_movel_curta = []
    fmedia_movel_longa = []

    for i in range(len(vRepeticao)):
        # Média móvel curta (janela 2)
        if i >= vCofing['indicador']['mm'][0] - 1:
            janela_curta = vRepeticao[i - vCofing['indicador']['mm'][0] + 1: i + 1]
            fmedia_movel_curta.append(sum(janela_curta) / len(janela_curta))
        else:
            fmedia_movel_curta.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

        # Média móvel longa (janela 10)
        if i >= vCofing['indicador']['mm'][1] - 1:
            janela_longa = vRepeticao[i - vCofing['indicador']['mm'][1] + 1: i + 1]
            fmedia_movel_longa.append(sum(janela_longa) / len(janela_longa))
        else:
            fmedia_movel_longa.append(sum(vRepeticao[:i + 1]) / len(vRepeticao[:i + 1]))

    # Normalização para probabilidade (0-1)
    fprobabilidade_deox_curta = []
    fprobabilidade_deox_longa = []

    max_valor = max(vRepeticao) if vRepeticao else 1

    for i in range(len(fmedia_movel_curta)):
        if max_valor > 0:
            fprobabilidade_deox_curta.append(fmedia_movel_curta[i] / max_valor)
            fprobabilidade_deox_longa.append(fmedia_movel_longa[i] / max_valor)
        else:
            fprobabilidade_deox_curta.append(0)
            fprobabilidade_deox_longa.append(0)

    # Criar gráficos
    fig = iMatPlotLib_PyPlot.figure(figsize=(12, 8))

    # Gráfico 1: Repetições e médias móveis
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(vX, vRepeticao, 'b-', label='Repetição da Letra', linewidth=2)
    ax1.plot(vX, fmedia_movel_curta, 'r--', label=f"MM Curta ({vCofing['indicador']['mm'][0]})", linewidth=2)
    ax1.plot(vX, fmedia_movel_longa, 'g--', label=f"MM Longa ({vCofing['indicador']['mm'][1]})", linewidth=2)

    ax1.set_xlabel('Tempo/Índice')
    ax1.set_ylabel('Valor de Repetição')
    ax1.set_title('Análise de Repetições de Letras')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Probabilidades normalizadas
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(vX, fprobabilidade_deox_curta, 'r-', label='Probabilidade MM Curta', linewidth=2)
    ax2.plot(vX, fprobabilidade_deox_longa, 'g-', label='Probabilidade MM Longa', linewidth=2)

    ax2.set_xlabel('Tempo/Índice')
    ax2.set_ylabel('Probabilidade Normalizada')
    ax2.set_title('Probabilidades Normalizadas das Médias Móveis')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    iMatPlotLib_PyPlot.tight_layout()
    iMatPlotLib_PyPlot.show()

    # Retorna resultados para análise posterior
    return {
        'dados_processados': dados,
        'media_movel_curta': fmedia_movel_curta,
        'media_movel_longa': fmedia_movel_longa,
        'probabilidade_curta': fprobabilidade_deox_curta,
        'probabilidade_longa': fprobabilidade_deox_longa
    }


# Dados de teste corrigidos
vFrinxn = [
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q', 'r'],  # Letras possíveis
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Tempos
    ['a', 'd', 'e', 'a', 'b', 'c', 'a', 'd', 'e', 'f', 'a', 'b', 'g', 'h', 'i', 'j'],  # Respostas
    {
        'a': 1, 'b': 1, 'c': 2, 'd': 2, 'e': 2, 'f': 3, 'g': 3,
        'h': 4, 'i': 4, 'j': 4, 'k': 5, 'm': 5, 'n': 6, 'o': 6,
        'p': 6, 'q': 7, 'r': 7
    }  # Ordem total
]

if __name__ == '__main__':
    print("Iniciando análise...")
    resultado = fun_final_deck(vFrinxn[0], vFrinxn[1], vFrinxn[2], vFrinxn[3])

    if resultado:
        print("\n=== Resultados da Análise ===")
        print(f"Número de pontos processados: {len(resultado['dados_processados']['vXTempo'])}")
        print(f"Média móvel curta (último valor): {resultado['media_movel_curta'][-1]:.3f}")
        print(f"Média móvel longa (último valor): {resultado['media_movel_longa'][-1]:.3f}")
        print(f"Probabilidade curta (último valor): {resultado['probabilidade_curta'][-1]:.3f}")
        print(f"Probabilidade longa (último valor): {resultado['probabilidade_longa'][-1]:.3f}")