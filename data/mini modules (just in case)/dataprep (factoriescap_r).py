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

data = pd.read_excel('fac_r.xlsx')

tmp = []
final = []

for i in range(len(data)):
    reg, okato = getokato2(data.iloc[i, 0])
    for j in range(1, data.shape[1]):
        tmp.append(reg)
        tmp.append(okato)
        tmp.append(data.columns[j]) # year
        tmp.append(data.iloc[i, j]) # factoriescap
        final.append(tmp)
        tmp = []


final = np.array(final)

cols = ['region', 'okato', 'year', 'factoriescap_r']
final = pd.DataFrame(final, columns=cols)

final = final[final['okato'] != 'nan']

final = final.astype({'factoriescap_r': 'float32', 'year': 'int32'})

final = final.sort_values(by=['okato', 'year'])

final.to_csv('factoriescap_r.csv', index=False)

print('done')