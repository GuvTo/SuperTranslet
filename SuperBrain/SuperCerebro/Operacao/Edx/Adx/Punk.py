import SuperBrain.SuperCerebro.Aprender.Edx.Lox.Zsx as iZsx
from SuperBrain.SuperCerebro.Aprender.Edx.Lox.Zsx import fconteudo


def fun_resposta(fconteudo_aprender,fParaA, fParaB, fSuperTipo, fconteudo_entrar):
    fconteudo_final_aprender = iZsx.fun_aprender_diow(fconteudo_aprender, fParaA, fParaB, fSuperTipo)
    fconteudo_final_entrar = iZsx.fun_aprender_diow(fconteudo_entrar, fParaA, fParaB, fSuperTipo)

    #
    fSuperTipoMeu = 'vconteudo'

    fconteudo_final_aprender2 = iZsx.fun_aprender_diow(fconteudo_aprender, fParaA, fParaB, fSuperTipo)
    fconteudo_final_entrar2 = iZsx.fun_aprender_diow(fconteudo_entrar, fParaA, fParaB, fSuperTipo)

    fconteudo_resposta = ''
    fconteudo_resposta_lista = []

    fNumProb = []
    fNumProb2 = []

    fEsPodeIr = False

    fEsPodeIrCont = 1

    xElk2 = 0

    fcont_super = 0
    fcont_super_extra = 0

    for xElk in range(len(fconteudo_final_aprender[3])):

        fcont_super = fcont_super_extra
        fcont_super_extra += 1



        vElk = fconteudo_final_aprender[3][xElk]

        vElk2 = vElk

        #xElk2 = 0

        if xElk == len(fconteudo_aprender[3]):
            xElk2 = xElk-1


        vElk2 = fconteudo_final_entrar[3][(xElk2)]

        fNumProb.append(vElk)

        fNumProb2.append(vElk2)

        # verificar probabilidade
        vElkFinal = ((vElk/vElk2))*10
        print('aqui:', vElkFinal)
        fEsPodeIr = vElkFinal > 50

        if ((fEsPodeIr == True)): #and (fEsPodeIrCont != 0)):
            #fconteudo_resposta = str(fconteudo_final_aprender2[2][0][xElk]['vconteudo'])
            #fconteudo_resposta_lista.append(fconteudo_resposta)

            print('eimx')


            fEsPodeIrCont += 1

            if fEsPodeIrCont >= 2:
                fEsPodeIrCont = 0
                fEsPodeIr = False

            fconteudo_resposta = str(fconteudo_final_aprender2[2][0][xElk]['vconteudo'])
            fconteudo_resposta_lista.append(fconteudo_resposta)




        else:
            fEsPodeIr = False
            fEsPodeIrCont = 0


    fconteudo_resposta_final_super = ''

    for xListax in range(len(fconteudo_resposta_lista)):
        if fconteudo_entrar.strip() in fconteudo_resposta_lista[xListax]:
            fconteudo_resposta_final_super = fconteudo_resposta_lista[xListax]

            break






    return [0, fconteudo_resposta, fconteudo_resposta_lista, fconteudo_resposta_final_super]


if __name__ == '__main__':

    fconteudo_aprenderT = '1+1=2 A+A=B NOME=GUSTAVO IDADE=18 NOME=THAINA '
    fconteudo_entrarT = 'THAINA '

    #

    fLetra_A = iZsx.fletra_A
    fLetra_B = iZsx.fletra_B

    #

    vEdk = fun_resposta(fconteudo_aprenderT, fLetra_A, fLetra_B, 'vtipo2', fconteudo_entrarT)

    print(vEdk[3])

