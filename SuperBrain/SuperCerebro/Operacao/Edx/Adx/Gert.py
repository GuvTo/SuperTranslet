import SuperBrain.SuperCerebro.Operacao.Edx.Adx.Punk as iPunk

def fun_varias_resposta(finputs_aprender: list):
    vParaAprenderOutPut = []
    for xParaApreder in range(len(finputs_aprender)):
        fPrenderT = vParaAprenderOutPut[xParaApreder]
        fPrenderT_continuacao = fPrenderT.replace(' ', '_')
        vParaAprenderOutPut.append(fPrenderT_continuacao)

    vParaAprenderOutPut_final = ''

    for xParaApreder in range(len(vParaAprenderOutPut_final)):
        vParaAprenderOutPut_final += vParaAprenderOutPut[xParaApreder] + ' '


    return [0, vParaAprenderOutPut_final]


def fun_resposta_final(fconteudo_aprender,fParaA, fParaB, fSuperTipo, fconteudo_entrar):
    fconteudo_aprender_meio = fun_varias_resposta(fconteudo_aprender)[1]
    #fconteudo_aprender_meio += ' '
    fconteudo_aprender_final = list(fconteudo_aprender_meio.split(' '))

    fconteudo_aprender_meio += ' '

    fconteudo_entrar_meio = fun_varias_resposta(fconteudo_entrar)[1]
    #fconteudo_entrar_meio += ' '
    fconteudo_entrar_final = list(fconteudo_entrar_meio.split(' '))

    fresposta_total = ''

    for xUserEntrar in range(len(fconteudo_entrar_final)):
        fresposta_total += iPunk.fun_resposta(fconteudo_aprender_meio, fParaA, fParaB, fSuperTipo, fconteudo_entrar_final[xUserEntrar] + ' ')




    return [0, fresposta_total]


