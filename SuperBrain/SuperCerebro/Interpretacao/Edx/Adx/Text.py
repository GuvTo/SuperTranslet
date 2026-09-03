"""

data: 29/08/2026 - 19:35

"""

#import numpy as np
#import pandas as pd

import random as rd

def fcatalogar(fleitura: str): # função para catalogar dados qualquer em conjutos
    vLerTed = ''
    fleitura += ' '
    vOrdem = 0
    vOrdemSub = 0

    vLerTedExtra = ''

    vTipo = []
    vNome = []
    vConteudo = []
    vNumeroOrdem = []
    vLerTed2 = ''

    vCont = 0
    vContSub = 0

    vLerTed2 = ''

    vCont3 = 0
    vContSub3 = 0

    vCont4 = 0
    vContSub4 = 0

    vTerminouLogiteck = False

    """
    tipos:
        1: espaço
        2: numero
        3: alfabetico
        4: ordem
            1: reverter
            2: adicionar
        5: simbolo
    
    """

    for xLerTed in range(len(fleitura)-1):
        #vLerTed += fleitura[vCont]

        vCont = vContSub
        vContSub += 1

        if vOrdemSub >= 1:
            vLerTed = fleitura[vCont]
            vLerTed2 = vLerTed
            if vContSub3 == 0:
                vContSub3 = vCont

        else:
            if vOrdemSub <= 0:
                vLerTed = fleitura[vCont]
                vOrdemSub = 0
                vLerTed2 = ''
                vCont3 = vCont
                #vContSub3 = 0


        #vOrdemSub = 0
        if ' ' == vLerTed and vOrdemSub == 0:
            vOrdemSub = 1
            vConteudo.append(vLerTed)
            vNome.append(str(rd.randint(1+vCont,1000+vCont)+vCont))
            vTipo.append(1)
            vCont4 += 1

            vLerTed = ''

            print('dog')

            continue






        #vLerTed = vLerTed.strip()

        if vLerTed != ' ':

            vLerTedExtra += vLerTed


            if vOrdemSub == 1:
                #vLerTedExtra += vLerTed


                vTerminouLogiteck = (vLerTedExtra == fleitura.split(' ')[vCont4])
                print(str(fleitura.split(' ')[vCont4]))
                if vTerminouLogiteck == False:
                    #vLerTed  = ''


                    #vLerTedExtra += vLerTed
                    vOrdemSub = 0

                    print('xis')

                    continue


                    #...

                else:

                    if vTerminouLogiteck == True:



                        #vLerTed = ''
                        #vLerTedExtra = ''
                        #vTerminouLogiteck = False
                        vOrdemSub = 1
                        vTerminouLogiteck = False
                        print('aqui')
                        continue

                #vLerTedExtra += vLerTed
                print('fux')
                vOrdemSub = 0






            if vLerTedExtra.isnumeric() == True:
                vConteudo.append(vLerTedExtra.strip())
                vNome.append(str(rd.randint(1 + vCont, 1000 + vCont)+vCont))
                vTipo.append(2)

                vLerTedExtra = ''
                #vLerTed = ''

                continue

            if vLerTedExtra.isalpha() == True:
                print('alfabeto')
                vConteudo.append(vLerTedExtra)
                vNome.append(str(rd.randint(1 + vCont, 1000 + vCont)+vCont))
                vTipo.append(3)
                print('vcont:', vConteudo)

                vLerTedExtra = ''
                #vLerTed = ''

                continue

            else:
                #
                vConteudo.append(vLerTedExtra.strip())
                vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                vTipo.append(5)

                #vLerTedExtra = ''
                # vLerTed = ''


                vOrdemSub = 5
                #vLerTedExtra = ''
                #vLerTed = ''


        else:
            if '_:ordem' == vLerTed.strip() or vOrdemSub >= 4:
                #vLerTedExtra = ''
                #vLerTed = ''
                if vOrdemSub >= 4:
                    vLerTed2 = ''#vLerTed
                    #vLerTed2 = vLerTed2.strip()
                    #vLerTed = ''

                vOrdemSub = 0
                if vLerTed2.strip() == 'add':
                    vOrdemSub = 5
                    vLerTed2 = ''
                    #vLerTed = ''


                if vLerTed2.strip() == 'sub':
                    vOrdemSub = 6
                    vLerTed2 = ''
                    #vLerTed = ''

                if vLerTed2.strip() == 'extra':
                    vOrdemSub = 7
                    vLerTed2 = ''
                    #vLerTed = ''

                else:
                    if len(vLerTed) >= 1:
                        vConteudo.append(vLerTed.strip())
                        vNome.append(str(rd.randint(1 + vCont, 1000 + vCont)+vCont))
                        vTipo.append(vOrdemSub)
                        vOrdemSub = 0

                        #vLerTed = ''
                        continue

                    else:
                        vLerTed2 += vLerTed
                        #vLerTed = ''

                        #vOrdemSub = 0



            if '_:final' == vLerTed.strip():
                vOrdemSub = 0
                #vLerTed = ''
                continue

            else:
                """"
                vConteudo.append(vLerTed.strip())
                vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                vTipo.append(3)
                vLerTed = ''


                continue
                """

                #
                vConteudo.append(vLerTed2)
                vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                vTipo.append(3)



                # vLerTedExtra = ''
                # vLerTed = ''

                vOrdemSub = 5
                vLerTedExtra = ''
                # vLerTed = ''
                continue




    vConteudo_Geral = {
        'vAprendizado':{
            'vConteudo':vConteudo,
            'vNome':vNome,
            'vTipo':vTipo,
            'vConteudoTotal':fleitura

        }
    }

    return vConteudo_Geral



print(fcatalogar(' olá, como vai? _:ordem add olá _:final '))