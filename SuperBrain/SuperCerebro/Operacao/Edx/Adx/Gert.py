import SuperBrain.SuperCerebro.Operacao.Edx.Adx.Punk as iPunk

def fun_varias_resposta(finputs_aprender: list):
    vParaAprenderOutPut = []
    for xParaApreder in range(len(finputs_aprender)):

        fPrenderT = finputs_aprender[xParaApreder]

        #if fPrenderT == ' ':
        #    fPrenderT = '_'

        fPrenderT_continuacao = fPrenderT.replace(' ', '_')
        vParaAprenderOutPut.append(fPrenderT_continuacao)

    vParaAprenderOutPut_final = ''

    for xParaApreder in range(len(vParaAprenderOutPut)):
        vParaAprenderOutPut_final += vParaAprenderOutPut[xParaApreder]


    #vParaAprenderOutPut_final = ''

    vParaAprenderOutPut_final.strip()
    print('Xis:', vParaAprenderOutPut_final)


    return [0, vParaAprenderOutPut_final]

#def fun_mini_separa(ftexto):
#    ftexto_final


def fun_resposta_final(fconteudo_aprender,fParaA, fParaB, fSuperTipo, fconteudo_entrar):
    fconteudo_aprender_meio = fun_varias_resposta(fconteudo_aprender)[1]
    #fconteudo_aprender_meio += ' '
    fconteudo_aprender_final = (fconteudo_aprender_meio.split(' '))

    fconteudo_aprender_meio += ' '

    fconteudo_entrar_meio = fun_varias_resposta(fconteudo_entrar)[1]
    #fconteudo_entrar_meio += ' '
    fconteudo_entrar_final = fconteudo_entrar_meio#.split(' ')

    fresposta_total = ''

    xUserEntrar = 0

    xUserEntrar2 = 0

    fresposta_TAX = []

    faprenndexx = ''

    for xEntrxAprendx in fconteudo_aprender:
        faprenndexx += fun_varias_resposta(xEntrxAprendx)[1] + ' '

    for xaUserEntrar in range(len(fconteudo_entrar)):

        xUserEntrar = xaUserEntrar
        print('uiddj', xUserEntrar)

        '''
        if xUserEntrar >= len(fconteudo_entrar):
            xUserEntrar = 0
            #continue



        else:
            xUserEntrar = xaUserEntrar
            
            
        '''
            

        '''
        if xUserEntrar2 != len(fconteudo_aprender):
            xUserEntrar2 += 1

        if xUserEntrar2 >= len(fconteudo_aprender):
            xUserEntrar2 = 0
            #continue

        #xUserEntrar -= 1
        #xUserEntrar2 -= 1

        if xUserEntrar2 <= 0:
            xUserEntrar2 = 0
            
        '''

        print('ekmwd', xUserEntrar2)

        fresposta_TAX.append(iPunk.fun_resposta(faprenndexx, fParaA, fParaB, fSuperTipo, fconteudo_entrar[xUserEntrar] + ' ')[3])

        fresposta_total = str(fresposta_TAX[-1])

        print(str(fconteudo_aprender_final) + '+' + fconteudo_entrar_final[xUserEntrar])





    return [0, fresposta_total]


