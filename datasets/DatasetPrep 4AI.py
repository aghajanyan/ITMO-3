import csv
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

# нормализация знечений признаков от 0 до 1 (с сохранением файла с нормализаторами (макс.))
def normbymax(trainset):
    tmpp = []
    for k in range(3, len(trainset[0])):
        maxi = trainset[0][k]
        for i in range(len(trainset)):
            if (maxi < trainset[i][k]):
                maxi = trainset[i][k]

        tmpp.append(maxi)

        for j in range(len(trainset)):
            trainset[j][k] = trainset[j][k] / maxi

    features = ['VDS_s', 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s',
                  'RDcosts_s', 'RDsalary_s']

    tmpp = np.array(tmpp)
    tmpp = pd.DataFrame([tmpp], columns=features)
    tmpp.to_csv("fornorm VDS_s.csv", index=False)

    return trainset

# умножить рублевые признаки на соответствующую долю инфляции
def normbyinf(trainset, rubfeatures):
    inflation = pd.read_csv("inflation16-24.csv")
    trainset = trainset.merge(inflation, on='year', how='left')
    inf = trainset[['inf']]
    for k in range(len(rubfeatures)):
        tmp = trainset[[rubfeatures[k]]]
        for i in range(len(tmp)):
            try:
                infnorm = 1 - (inf.iloc[i, 0] / 100)
                tmp.iloc[i, 0] = float(tmp.iloc[i, 0]) * infnorm
            except ValueError:
                tmp.iloc[i, 0] = tmp.iloc[i, 0]
        trainset[rubfeatures[k]] = tmp
        tmp = pd.DataFrame(None)
    trainset = trainset[trainset.columns.drop('inf')]
    return trainset



features = ['VDS_s', 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s',
                  'RDcosts_s', 'RDsalary_s']

# признаки для ценового нормирования
allrubfeatures = ['VDS_s', 'AIcosts_s' 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s',
                  'RDcosts_s', 'RDsalary_s', 'RDequip_s', 'factoriescap_s']

# получение и сортировка данных
rawdata = pd.read_csv("../data/VDS_s.csv")
rawdata = rawdata.sort_values(by=['okved2', 'year'])

tempset = []
for k in range(len(features) - 1):
    tempset = pd.read_csv('../data/'+features[k + 1]+'.csv')
    tempset = tempset[tempset.columns.drop('sector')]
    rawdata = rawdata.merge(tempset, on=['okved2', 'year'], how='left')

rawdata = rawdata.dropna()

rawdata = normbyinf(rawdata, features)

rawdata = np.array(rawdata)
rawdata = normbymax(rawdata)

features = ['sector', 'okved2', 'year', 'VDS_s', 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s',
            'RDcosts_s', 'RDsalary_s']

rawdata = pd.DataFrame(rawdata, columns=features)
rawdata.to_csv('VDS_s.csv')

print('done')