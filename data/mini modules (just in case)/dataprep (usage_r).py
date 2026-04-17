import csv
import numpy as np
import pandas as pd

def getsector1(rawname):
    rawname = rawname.split('\n')
    rawname = rawname[1].split(' ', 1)
    return rawname[1]

def getsector2(rawname):
    rawname = rawname.rsplit(' ', 1)
    return rawname[0], rawname[1]

def getsector3(okved2, data):
    sector = ''
    for i in range(len(data)):
        if str(data.iloc[i, 1]).replace(' ', '') == okved2:
            sector = data.iloc[i, 0]
            break
    return sector

def getokato(region):
    okatodata = pd.read_excel('okato.xlsx',  dtype={'okato': str})
    okato = 'nan'
    for i in range(len(okatodata)):
        if region == okatodata.iloc[i, 0]:
            okato = okatodata.iloc[i, 1]
            break

    if okato == 'nan':
        return region, okato
    else:
        return region, okato

def getokato2(region):
    region = region.split(' ', 1)
    region = region[1].lstrip()

    okatodata = pd.read_excel('okato.xlsx', dtype={'okato': str})
    okato = 'nan'
    for i in range(len(okatodata)):
        if region == okatodata.iloc[i, 0]:
            okato = okatodata.iloc[i, 1]
            break

    if okato == 'nan':
        return region, okato
    else:
        return region, okato

year = 2016
data = pd.read_excel(''+str(year)+'.xlsx')

data = data.drop(data.index[0:7])
#data = data.iloc[:-2]   # удаление последних двух строк

tmp = []
final = []

for i in range(len(data)):
    reg, okato = getokato2(data.iloc[i, 0])
    tmp.append(reg)
    tmp.append(okato)
    tmp.append(year)
    tmp.append(data.iloc[i, 1]) # ITusage
    tmp.append(data.iloc[i, 7])  # inetusage
    tmp.append(data.iloc[i, 2])  # PCusage
    final.append(tmp)
    tmp = []


final = np.array(final)

cols = ['region', 'okato', 'year', 'ITusage_r', 'inetusage_r', 'PCusage_r']
final = pd.DataFrame(final, columns=cols)

final = final[final['okato'] != 'nan']

final = final.replace(to_replace='...', value=np.NAN)
final = final.replace(to_replace='…1)', value=np.NAN)
final = final.replace(to_replace='-', value=np.NAN)

final.to_csv(''+str(year)+'.csv', index=False)

print('done')