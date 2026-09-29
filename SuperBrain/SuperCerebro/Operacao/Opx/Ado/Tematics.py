'''

class cBrainUsuper:
    def __init__(self):
        self._set_vars_new()

    # variaveis
    def _set_vars_new(self):
        self._set_var_edk()
        self._set_var_aprendeck()

    def _set_var_edk(self):
        self._vPartesSuporteA = []
        self._vPartesSuporteTemasB = []

        self._vAprenderInput = []

        self._user_input = []

        self._local = []

    def _set_var_aprendeck(self):
        self._vTemas = []
        self._vTemasGeneralizado = []

    def _cofing_asLista(self):
        for xContex in range(len(self._vAprenderInput)):
            self._vTemasGeneralizado.append([])

    def _suportar_temas_aprender(self):
        vFinal = []

        for xAprendert in range(len(self._vAprenderInput)):
            # verificar tema
            vContar_tema = self._vTemas.count(self._vAprenderInput[xAprendert])

            if vContar_tema >= 1:
                self._vTemasGeneralizado[xAprendert].append(self._vAprenderInput[xAprendert])

            if vContar_tema <= 0:
                self._vTemas.append(self._vAprenderInput[xAprendert])
                self._vTemasGeneralizado[xAprendert].append(self._vAprenderInput[xAprendert])

            vTipoA = []
            vTipoB = []

            for xTiposA in range(len(self._vPartesSuporteA)):
                if self._vPartesSuporteA[xTiposA] in self._vAprenderInput[xAprendert]:
                    vTipoA.append(self._vPartesSuporteA[xTiposA])
                    vTipoB.append(self._vPartesSuporteTemasB[])

            self._local.append({
                'iindex':xAprendert,
                'itemas':self._vAprenderInput[xAprendert]
            })


'''
