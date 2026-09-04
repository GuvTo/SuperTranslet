"""

data criação: 04/09/2026 - 17:44


"""

# info

"""

dividir cada partes por espaço chamado de token, em uma lista

então
    - separar
        por
            tipo
            quantidade
            repetição
            nome
            conteudo
    os token
    
cada token terá subtoken

"""

#
import SuperBrain.SuperCerebro.Interpretacao.Edx.Adx.Ewx as iEwx
#

def fun_separar(fconteudo: str, fconjunto_tipo: str, fordem_conjuto_tipo: str):
    vConteudo = list(fconteudo.strip().split(' '))
    vConteudo_final = []

    vConjutoTipo = list(fconjunto_tipo.strip().split(' '))

    vOrdem_conjuto_tipo = list(fordem_conjuto_tipo.strip().split(' ')) # na mesma quantidade que  vConjutoTipo

   # vConjutoTipo.reverse() # aqui por enquanto remova caso de erro

    vTokens = []
    vSubtokens = []
    vIndex = 0

    vNome = []

    vQuantidade = []

    vTipo = []

    for xConteudo in range(len(vConteudo)):
        # variavel
        tConteudo = vConteudo[xConteudo]
        vIndex = xConteudo

        fTipo = ''
        fTipo_final = ''

        # tipo

        for xConjuto_tipo in range(len(vConjutoTipo)):
            for xConteudoDrex in tConteudo:
                if vConjutoTipo[xConjuto_tipo] == xConteudoDrex:
                    fTipo += (vOrdem_conjuto_tipo[xConjuto_tipo]) + ';Sep:' #+ ' ' + tConteudo + ' ' + vConjutoTipo[xConjuto_tipo])
                    fTipo_final += vConjutoTipo[xConjuto_tipo]
                else:
                    ...


        # tipo

        vTipo.append(fTipo + ' ' + fTipo_final)#(fTipo + ' ' + tConteudo + ' ' + fTipo_final)
        fSubToken = fTipo + ' ' + tConteudo + ' ' + fTipo_final

        # quantidade
        vQuantidade.append(vConteudo.count(tConteudo))

        # nome
        vNome.append(iEwx.fcatalogar(tConteudo + ' '))

        vConteudo_final.append(tConteudo)

        vConteudo_final.append(' ')

        vTokens.append(
            {
                'vtipo':vTipo[-1],
                'vquantidade':vQuantidade[-1],
                'vnome':vNome[-1]['vAprendizado']['vNome'],
                'vconteudo': vConteudo_final[-2],
                'vsubtokens':fSubToken

            }
        )

    return [vTokens]


if __name__ == '__main__':

    # Criando a string A com letras, números e operadores matemáticos
    # String B com os nomes correspondentes

    # Letras maiúsculas e minúsculas
    letras_maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letras_minusculas = "abcdefghijklmnopqrstuvwxyz"

    # Números de 0 a 9
    numeros = "0123456789"

    # Operadores matemáticos
    operadores = "+-*/^%="

    # Montando as strings
    A_parts = []
    B_parts = []

    # Adicionando letras maiúsculas e minúsculas
    for letra in letras_maiusculas + letras_minusculas:
        A_parts.append(letra)
        B_parts.append("letra")

    # Adicionando números (0 a 9)
    for numero in numeros:
        A_parts.append(numero)
        B_parts.append("numero")

    # Adicionando operadores matemáticos
    for operador in operadores:
        A_parts.append(operador)
        B_parts.append("operacao")

    # Juntando com espaços
    A = " ".join(A_parts)
    B = " ".join(B_parts)

    # Exibindo as strings
    print("String A:")
    print(A)
    print("\nString B:")
    print(B)

    # Verificação de igualdade de elementos
    elementos_A = A.split()
    elementos_B = B.split()

    print(f"\nTotal de elementos em A: {len(elementos_A)}")
    print(f"Total de elementos em B: {len(elementos_B)}")

    if len(elementos_A) == len(elementos_B):
        print("✅ As strings A e B têm o MESMO número de elementos!")
    else:
        print("❌ As strings NÃO têm o mesmo número de elementos!")

    # Mostrando a correspondência (primeiros 10 pares)
    print("\nCorrespondência (primeiros 10 pares):")
    for i in range(min(10, len(elementos_A))):
        print(f"  A[{i}] = '{elementos_A[i]}'  ->  B[{i}] = '{elementos_B[i]}'")

    #

    fconteudo = '1+1=2 OLA'
    fconjuto_tipo = A
    fordem_conjuto_tipo = B

    vvValorFinal = fun_separar(fconteudo, fconjuto_tipo, fordem_conjuto_tipo)

    vvConteudo_final = ''
    vvConteudo_final_super = ''
    vvNome_final = ''

    for xConteudos in vvValorFinal[0]:
        vvConteudo_final += xConteudos['vsubtokens'] + '~'
        vvConteudo_final_super += xConteudos['vconteudo'] + '~'
        vvNome_final += str(xConteudos['vnome'][0]) + '~'#['vAprendizado']['vNome'] + '~'

    print('subtokens', vvConteudo_final)
    print('conteudo', vvConteudo_final_super)
    print('nomes', vvNome_final )

