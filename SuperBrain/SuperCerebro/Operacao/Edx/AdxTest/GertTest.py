import SuperBrain.SuperCerebro.Operacao.Edx.Adx.Gert as iGert

def fun_teste_aprender_total(ffcontend_aprender, ffcontend_entrar):
    fcontend_aprender = ffcontend_aprender
    fcontend_entrar = ffcontend_entrar

    finput_sistem = ''
    foutput_sistem = ''

    fParaMeuA = iGert.iPunk.fLetra_A
    fParaMeuB = iGert.iPunk.fLetra_B

    fSuperMeuTipo = ''

    #for xContendEntrar in range(len(fcontend_entrar)):
    finput_sistem += 'in: ' + str(fcontend_entrar) + ' \n'
    foutput_sistem += 'out' + iGert.iPunk.fun_resposta(fcontend_aprender, fParaMeuA, fParaMeuB, fSuperMeuTipo, fcontend_entrar) + ' \n'

    print(finput_sistem)
    print('IAGeek')
    print(foutput_sistem)


if __name__ == '__main__':
    vAprender = []
    vEntrar = []

    fun_teste_aprender_total(vAprender, vEntrar)

