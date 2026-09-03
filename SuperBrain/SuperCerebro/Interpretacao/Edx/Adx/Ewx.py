"""

DATA: 30/08/2026

"""


import random as rd


def fcatalogar(fleitura: str):  # função para catalogar dados qualquer em conjutos
    fleitura += ' '  # Garante que a última palavra seja processada

    vTipo = []
    vNome = []
    vConteudo = []

    vLerTedExtra = ''
    vOrdemSub = 0
    vCont = 0

    """
    tipos:
        1: espaço
        2: numero
        3: alfabetico
        4: ordem (gatilho)
        5: simbolo / ordem add
        6: ordem sub
        7: ordem extra
    """

    for xLerTed in range(len(fleitura) - 1):
        vLerTed = fleitura[vCont]
        vCont += 1

        if vLerTed == ' ':
            # 1. Cataloga o espaço
            vConteudo.append(' ')
            vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
            vTipo.append(1)

            # 2. Cataloga a palavra/símbolo acumulado
            if vLerTedExtra:
                if vLerTedExtra == '_:final':
                    vOrdemSub = 0
                    vLerTedExtra = ''
                    continue

                elif vLerTedExtra == '_:ordem':
                    vOrdemSub = 4  # Entra no estado de espera de comando
                    vLerTedExtra = ''
                    continue

                elif vOrdemSub == 4:
                    # Processa os comandos de ordem
                    if vLerTedExtra == 'add':
                        vTipo.append(5)
                    elif vLerTedExtra == 'sub':
                        vTipo.append(6)
                    elif vLerTedExtra == 'extra':
                        vTipo.append(7)
                    else:
                        vTipo.append(5)  # fallback para símbolo se não for um comando válido

                    vConteudo.append(vLerTedExtra)
                    vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                    vOrdemSub = 0
                    vLerTedExtra = ''
                    continue

                # Verifica o tipo do conteúdo acumulado
                elif vLerTedExtra.isnumeric():
                    vConteudo.append(vLerTedExtra)
                    vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                    vTipo.append(2)

                elif vLerTedExtra.isalpha():
                    vConteudo.append(vLerTedExtra)
                    vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                    vTipo.append(3)

                else:
                    vConteudo.append(vLerTedExtra)
                    vNome.append(str(rd.randint(1 + vCont, 1000 + vCont) + vCont))
                    vTipo.append(5)

                vLerTedExtra = ''
        else:
            # Acumula os caracteres até encontrar um espaço
            vLerTedExtra += vLerTed

    vConteudo_Geral = {
        'vAprendizado': {
            'vConteudo': vConteudo,
            'vNome': vNome,
            'vTipo': vTipo,
            'vConteudoTotal': fleitura
        }
    }

    return vConteudo_Geral


if __name__ == '__main__':


    # Chamada da função corrigida (sem o parêntese extra)
    print(fcatalogar('olá, como vai? _:ordem add olá _:final '))