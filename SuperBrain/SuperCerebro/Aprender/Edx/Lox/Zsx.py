#


#

import SuperBrain.SuperCerebro.Interpretacao.Edx.Axov.Linz as iLinz

import scipy as iSciPy

import pandas as pd

import statsmodels as iStatsModels

fletra_A = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z ' + '0 1 2 3 4 5 6 7 8 9 ' + '+ - * / ^ % = ' + '. ? ! ' + '_ ' + '['
fletra_B = '1 '*26 + '2 '*26 + '3 '*9 + '4 '*7 + '5 '*3 + '6 '+ '7'

fconteudo = 'ola como vai ja vai '

#fconteudo_final = iLinz.fun_separar(fconteudo, fletra_A, fletra_B)

def fun_aprender_diow(fconteudo_aprender, fParaA, fParaB, fvSuperTipo):
    fconteudo_final = iLinz.fun_separar(fconteudo_aprender, fParaA, fParaB)
    vDados_para_aprender = pd.DataFrame(fconteudo_final[0])

    vTipoEst = vDados_para_aprender.columns#['vtipo2']

    vAprender_dex = []

    vTipoEstValor = 0

    for xTipoEst in range(len(vTipoEst)):
        #vTipoEstValor += 2

        #vTipoEstValorDois = vTipoEstValor-xTipoEst

        #vTipoEstValorDois -= 1

        if xTipoEst == len(fconteudo_aprender.split(' '))-1:
            break


        vAprender_dex.append(vDados_para_aprender[fvSuperTipo][xTipoEst].mean())#['vsubtokens'].median(vTipoEst[xTipoEst]))
        print('cvv', str(xTipoEst))
        print('xxf:',vDados_para_aprender[fvSuperTipo][xTipoEst] )
        print('conteudo:', vDados_para_aprender['vconteudo'][xTipoEst])
        print('probabilidade:', vAprender_dex[-1])


    #print('+++')
    #print(vAprender_dex)
    #print('+==+')
    #print(vDados_para_aprender)
    #print('+')
    #print(fconteudo_final)
    '''print(f"""

    tipo estatistica:
    {vTipoEst}

            """)
            
    '''

    return [0,vDados_para_aprender, fconteudo_final, vAprender_dex]


if __name__ == '__main__':
    vElk = fun_aprender_diow(fconteudo, fletra_A, fletra_B, 'vtipo2')

    for xElk in range(len(vElk[3])):
        print('A:' + str(vElk[3][xElk]))