import random as iRd

def ffun_primos(vx):
    vValorFinal = ((vx**3)-(vx*(vx-1)))/vx

    #vValorFinal += 3*vx

    #vValorFinal -= 3*vx

    """

    if vValorFinal == 2 or vValorFinal == 1:
        vValorFinal -= 3
    if int(vValorFinal)%3 == 0:
        vValorFinal += 2

    if int(vValorFinal)%2 == 0:
        vValorFinal += vx-2
        
    else:
        vValorFinal -= vx+2
        
    
    """




    return vValorFinal

def fEdk_egc(vRepeticao: int, vOqueFazer):
    vListaResultados = []

    for xInxt in range(vRepeticao):
        vListaResultados.append((ffun_primos(xInxt+1)+vOqueFazer)-(xInxt-1))

    return vListaResultados

print(f"""

RESULTADOS PARA POSSIVEIS PRIMOS:
    :[{fEdk_egc(100, 0)}];

""")

with open(f'primos_edk_e{iRd.randint(0, 100000)}ds.txt', 'w') as vOpsc:
    vOpsc.write(str(fEdk_egc(1000000, 0)))

    vOpsc.close()