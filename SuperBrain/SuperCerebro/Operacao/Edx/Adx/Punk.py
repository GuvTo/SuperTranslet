import SuperBrain.SuperCerebro.Aprender.Edx.Lox.Zsx as iZsx

def fun_resposta(fconteudo_aprender,fParaA, fParaB, fSuperTipo, fconteudo_entrar):
    fconteudo_final_aprender = iZsx.fun_aprender_diow(fconteudo_aprender, fParaA, fParaB, fSuperTipo)
    fconteudo_final_entrar = iZsx.fun_aprender_diow(fconteudo_entrar, fParaA, fParaB, fSuperTipo)

    fconteudo_resposta = ''

    for xElk in range(len(fconteudo_final_aprender)):
        print('A:' + str(vElk[3][xElk]))