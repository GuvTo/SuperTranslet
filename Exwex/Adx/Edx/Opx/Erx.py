import pandas as pd
import numpy as np
import sklearn as iSk
import statsmodels as iStatsModel
import matplotlib as iMatPlotLib
import scipy as iSciPy
#
import statsmodels.stats.api as iStatsModel_stats
import statsmodels.formula.formulatools as iStatsModel_formula
#
import matplotlib.pyplot as iMatPlotLib_PyPlot
import matplotlib.streamplot as iMatPlotLib_edk

def fun_grafico(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):

    fvalor_x_tempo = []
    fvalor_y_repeticao = []
    fvalor_y_intensidadeOuLetra = []

    fOrdemRepeticao = []

    frepeticao_cont = 0
    frepeticao_cont2 = 0

    fsuper_parar = False

    for xTempo in range(len(vTempoLetra)):

        fvalor_x_tempo.append(vTempoLetra[xTempo])

        frepeticao_cont = 0

        for xResposta in range(len(vRespostas)):



            for xLetraRepeticao in range(len(vLetraRepeticao)):
                if (vRespostas[xResposta] == vLetraRepeticao[xLetraRepeticao]):
                    frepeticao_cont += 1

                    fvalor_y_repeticao.append( ((frepeticao_cont+len(vLetraRepeticao))-len(vLetraRepeticao)) )
                    fvalor_y_intensidadeOuLetra.append(vRespostas[xResposta])

                    fOrdemRepeticao.append(vOrdemTotal[f'{vRespostas[xResposta]}'])

                    #fsuper_parar = True

                    #

                    #


    fvalor_resultado_final = [{
        'vXTempo':fvalor_x_tempo,
        'vYRepeticao':fvalor_y_repeticao,
        'vYLetra':fvalor_y_intensidadeOuLetra,
        'vRepeticao':fOrdemRepeticao
    }]

    return [fvalor_resultado_final]



"""
def fun_calculo_final(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):
    fResultedck = fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal)

    fResultedck_meio_pandas = pd.DataFrame(fResultedck)

    fResultedck_final_pandas = fResultedck_meio_pandas#pd.Series(fResultedck_meio_pandas)

    fResultedck_final_pandas_series = pd.Series(fResultedck_final_pandas[0][0]['vRepeticao'])

    print(fResultedck_final_pandas[0][0]['vRepeticao'])

    fmedia_movel = fResultedck_final_pandas[0][0]['vRepeticao']. #fResultedck_final_pandas_series.rolling(window=(fResultedck_final_pandas[0][0]['vRepeticao'])).mean()



    fResultado_meio = []

    print(fmedia_movel)
    





if __name__ == '__main__':
    fun_calculo_final(['a', 'b'], [1], ['a', 'b','a', 'a'], {
        'a':1,
        'b':2
    })

"""

def fun_final_deck(vLetraRepeticao: list, vTempoLetra: list, vRespostas: list, vOrdemTotal: dict):
    vResux = fun_grafico(vLetraRepeticao, vTempoLetra, vRespostas, vOrdemTotal)

    vCofing = {
        'indicador':{
            'mm':[2, 10],
        }
    }

    fescolhas = [7, 3, 2]

    fcont_total = 0

    # para media movel
    fmedia_movel = [0, [], []]
    fprobabilidade_deox = [0,[], []]

    fvalor_x = []
    for xRetrux in vResux[0][0]['vRepeticao']:
        fmedia_movel[0] += xRetrux
        fmedia_movel[1].append((fmedia_movel[0])/vCofing['indicador']['mm'][0])
        fmedia_movel[2].append((fmedia_movel[0])/vCofing['indicador']['mm'][1])
        # probabilidade

        fcont_total += 1

        fvalor_x.append(fcont_total)

    for xFix in range(len(fmedia_movel[1])):
        fprobabilidade_deox[1].append(fmedia_movel[1][xFix]/fmedia_movel[0])
        #
        fprobabilidade_deox[2].append(fmedia_movel[2][xFix] / fmedia_movel[0])

    vRix = iMatPlotLib.pyplot.Axes().plot(fvalor_x, vResux[0][0]['vRepeticao'])


    vRix_sub = iMatPlotLib.pyplot.Axes().plot(fvalor_x, (fmedia_movel[1]))
    vRix_sub_p2 = iMatPlotLib.pyplot.Axes().plot(fvalor_x, fmedia_movel[2])

    vRix_sub2 = iMatPlotLib.pyplot.Axes().plot(fvalor_x, fprobabilidade_deox[1])
    vRix_sub2_p2 = iMatPlotLib.pyplot.Axes().plot(fvalor_x, fprobabilidade_deox[2])

    #vGrafique = iMatPlotLib.pyplot.subplot((vRix, vRix_sub, vRix_sub2))






vFrinxn = [
    ['a b c d e f g h i j k m n o p k q r'.split(' ')],
    [1],
    ['a', 'd', 'e'],
    {
        'a':1,
        'b':1,
        'c':2,
        'd':2,
        'e':2,
        'f':3,
        'g':3,
        'h':4,
        'i':4,
        'j':4,
        'k':5,
        'm':5,
        'n':6,
        'o':6,
        'p':6,
        'q':7,
        'r':7,

    },
]

if __name__ == '__main__':
    fun_final_deck(vFrinxn[0], vFrinxn[1], vFrinxn[2], vFrinxn[3])

