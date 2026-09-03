import SuperBrain.SuperCerebro.Interpretacao.Edx.Adx.Ewx as iEwx

import sklearn.metrics as iSklearn_Metrics

import matplotlib as iMtPltLb

import statsmodels.api as iSm

from math import sqrt

from statsmodels.tsa.ar_model import AR

import pandas as pd

vDadosFinal = """

    1+1=2
    2+2=4

"""

vDadosTreinamento = pd.DataFrame(iEwx.fcatalogar(vDadosFinal))

#vDataSetData = iSm.datasets.sunspots.load_pandas()

vSetTrain_ration = 0.8

#vTrain = vDadosTreinamento[:int(vSetTrain_ration*(len(vDadosTreinamento)))]

#vTest = vDadosTreinamento.
print(vDadosTreinamento.items)
print('+++')
print(vDadosTreinamento.to_json())