import SuperBrain.SuperCerebro.Operacao.Edx.Adx.Gert as iGert

def fun_teste_aprender_total(ffcontend_aprender, ffcontend_entrar):
    fcontend_aprender = ffcontend_aprender
    fcontend_entrar = ffcontend_entrar

    finput_sistem = ''
    foutput_sistem = ''

    fParaMeuA = iGert.iPunk.iZsx.fletra_A
    fParaMeuB = iGert.iPunk.iZsx.fletra_B

    fSuperMeuTipo = 'vtipo2'

    for xContendEntrar in range(len(fcontend_entrar)):

        print(f'''
        
        
        ''')
        finput_sistem += 'in: ' + str(fcontend_entrar[xContendEntrar]) + ' \n'
        foutput_sistem += 'out' + str(iGert.fun_resposta_final(fcontend_aprender, fParaMeuA, fParaMeuB, fSuperMeuTipo, fcontend_entrar[xContendEntrar])[1]) + ' \n'

    print(finput_sistem)
    print('IAGeek')
    print(foutput_sistem)


if __name__ == '__main__':
    vAprender = ['1+1 = 2.', 'A+A = B.']
    vEntrar = ['1+1', 'A+A', 'OP', '1+1']

    fun_teste_aprender_total(vAprender, vEntrar)

