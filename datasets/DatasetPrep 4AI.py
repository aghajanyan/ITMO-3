import csv
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from dask_expr import DataFrame
from sympy import false
import copy
import scipy.stats as sts
import seaborn as sns


# нормализация знечений признаков от 0 до 1 (с сохранением файла с нормализаторами (макс.))
def normbymax(rawdata, cols, datasetname):

    maxi = []
    for a in cols:
        maxi.append(rawdata[a].max())
        rawdata[a] = rawdata[a] / rawdata[a].max()

    maxi = np.array(maxi)
    maxi = pd.DataFrame([maxi], columns=cols)
    maxi.to_csv('fornorm '+ datasetname +'.csv', index=False)

    return rawdata

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

# IQR от Кирилла
def remove_outliers(data: pd.DataFrame) -> pd.DataFrame:
    data = copy.deepcopy(data)

    for col in data.columns:
        if col != 'region' and col != 'year' and col != 'okato':
            data = data[(data[col] < np.quantile(data[col], 0.75) + 4 * sts.iqr(data[col])) &
                        (data[col] > np.quantile(data[col], 0.25) - 4 * sts.iqr(data[col]))]

    return data

# Анализ зависимости отдельных признаков от определяющего
def visanalysis(rawdata):
    rawdata = rawdata.sort_values(by=['VDS_r']).reset_index(drop=True)
    #rawdata = rawdata[:int(len(rawdata) / 2)]

    #rawdata['skvozcosts_r'] = rawdata['skvozcosts_r'] / rawdata['ITcosts_r']
    rawdata['ITcosts_r'] = rawdata['ITcosts_r'] / rawdata['VDS_r']

    rawdata['VDS_r'] = rawdata['VDS_r'] / rawdata['VDS_r'].max()
    rawdata['ITcosts_r'] = rawdata['ITcosts_r'] / rawdata['ITcosts_r'].max()
    #rawdata['skvozcosts_r'] = rawdata['skvozcosts_r'] / rawdata['skvozcosts_r'].max()

    plt.scatter(rawdata['VDS_r'], rawdata['ITcosts_r'], marker='o')
    # plt.plot(rawdata['factoriescap_s'])
    # plt.plot(rawdata['skvozcosts_s'])
    # plt.plot([0, 1], [0, 1], ls='--', c='red', label='Linear')
    plt.show()

# Чистка датасета от выбросов (определенных визуально)
def visnorm(rawdata):
    # на основе визуальной нормализации
    rawdata = rawdata[rawdata['okved2'] != 'C']
    #rawdata = rawdata[(rawdata['okved2'] != '19') | (rawdata['year'] != 2022)]
    awdata = rawdata[(rawdata['okved2'] != '19') | (rawdata['year'] != 2023)]

    #rawdata = rawdata[(rawdata['okved2'] != '19.2') | (rawdata['year'] != 2022)]
    #rawdata = rawdata[(rawdata['okved2'] != '19.2') | (rawdata['year'] != 2023)]

    #rawdata = rawdata[(rawdata['okved2'] != '08') | (rawdata['year'] != 2021)]
    rawdata = rawdata[(rawdata['okved2'] != 'B') | (rawdata['year'] != 2021)]

def regionanalysis(rawdata, features):

    rawdata = normbyinf(rawdata, features)
    rawdata = rawdata.sort_values(by=['okato', 'VDS_r'], ascending=[True, False])
    rawdata = rawdata.reset_index(drop=True)

    year = 2020
    for i in range(5):
        rawdata['year'].loc[rawdata['year'] == year] = i
        year +=1

    okato = rawdata['okato'].unique()

    neworder = ['region', 'okato' ,'VDS_r', 'year', 'ITcosts_r', 'skvozcosts_r', 'trainingcosts_r']
    rawdata = rawdata[neworder]
    final = pd.DataFrame()
    for a in okato:
        temp = rawdata[rawdata['okato'] == a]
        for col in temp.columns:
            if col != 'okato' and col != 'region':
                temp[col] = temp[col] / temp[col].max()

        final = pd.concat([final, temp])
        final.loc[len(final)] = np.nan

    with pd.ExcelWriter('regions analysis.xlsx', engine='openpyxl') as writer:
        rawdata.to_excel(writer, sheet_name='regions', index=False)
        final.to_excel(writer, sheet_name='patterns', index=False)

def separatesector(rawdata, features):
    sepsector = []
    for i in range(len(rawdata)):
        try:
            if int(rawdata.iloc[i, 1]) >= 41 and int(rawdata.iloc[i, 1]) <= 43:
                sepsector.append(rawdata.iloc[i])
        except ValueError:
            pass

    sepsector = pd.DataFrame(sepsector)
    sepsector = sepsector.reset_index(drop=True)
    sepsector = normbyinf(sepsector, features)

    sepsector['skvozcosts_s'] = sepsector['skvozcosts_s'] / sepsector['ITcosts_s']
    sepsector['trainingcosts_s'] = sepsector['trainingcosts_s'] / sepsector['ITcosts_s']
    #sepsector['ITcosts_s'] = sepsector['ITcosts_s'] / sepsector['factoriescap_s']

    #sepsector['RDsalary_s'] = sepsector['RDsalary_s'] / sepsector['RDcosts_s']
    #sepsector['RDequip_s'] = sepsector['RDequip_s'] / sepsector['RDcosts_s']


    sepsector.to_excel('construction sector (factoriescap_s) 0.xlsx', index=False)

features = ['VDS_r', 'ITcosts_r', 'skvozcosts_r', 'trainingcosts_r']


# признаки для ценового нормирования
allrubfeatures = ['VDS_s', 'AIcosts_s' 'ITcosts_s', 'skvozcosts_s', 'trainingcosts_s',
                  'RDcosts_s', 'RDsalary_s', 'RDequip_s', 'factoriescap_s']

allrubfeatures_r = ['VDS_r', 'AIcosts_r' 'ITcosts_r', 'skvozcosts_r', 'trainingcosts_r',
                  'RDcosts_r', 'RDsalary_r', 'RDequip_r', 'factoriescap_r']


datasetname = 'agro-sector'

# получение и сортировка данных
rawdata = pd.read_csv("../data/VDS_r.csv", dtype={'okato': str})
#rawdata = pd.read_csv("../data/VDS_r.csv")
rawdata = rawdata.sort_values(by=['okato', 'year'])

tempset = []
for k in range(1, len(features)):
    tempset = pd.read_csv('../data/'+features[k]+'.csv', dtype={'okato': str})
    #tempset = pd.read_csv('../data/' + features[k] + '.csv')
    tempset = tempset[tempset.columns.drop('region')]
    rawdata = rawdata.merge(tempset, on=['okato', 'year'], how='left')

rawdata = rawdata.dropna()

# Анализ регионов (подготовка данных под паттерн-анализ)
regionanalysis(rawdata, features)

# Выделить отдельный сектор в эксель файл для анализа
#separatesector(rawdata, features)

minyear = rawdata['year'].min()
rawdata = normbyinf(rawdata, ['factoriescap_s'])

#visanalysis(rawdata)
rawdata['AIusage_r'] = rawdata['AIusage_r'] / rawdata['ITusage_r']
rawdata['BDusage_r'] = rawdata['BDusage_r'] / rawdata['ITusage_r']
rawdata = rawdata[rawdata.columns.drop('ITusage_r')]
features.remove('ITusage_r')

"""
rawdata['skvozcosts_r'] = rawdata['skvozcosts_r'] / rawdata['ITcosts_r']
rawdata['trainingcosts_r'] = rawdata['trainingcosts_r'] / rawdata['ITcosts_r']
rawdata['ITcosts_r'] = rawdata['ITcosts_r'] / rawdata['VDS_r']

rawdata['RDsalary_r'] = rawdata['RDsalary_r'] / rawdata['RDcosts_r']
rawdata['RDequip_r'] = rawdata['RDequip_r'] / rawdata['RDcosts_r']
rawdata['RDcosts_r'] = rawdata['RDcosts_r'] / rawdata['VDS_r']
"""

rawdata = remove_outliers(rawdata)

rawdata = normbymax(rawdata, features, datasetname)

#features = ['sector', 'okved2', 'year', 'VDS_r', 'ITcosts_r', 'skvozcosts_r', 'trainingcosts_r']

#rawdata = pd.DataFrame(rawdata, columns=features)
rawdata.to_csv(''+ datasetname +'.csv', index=False)

print('done')