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

data = pd.read_excel('2025s.xlsx')

tmp = []
final = pd.DataFrame()

data = data.drop(data.index[0:7])
data = data.iloc[:-3]

final['sector'] = data.iloc[:, 0]
final['okved2'] = data.iloc[:, 1]
final['year'] = 2025
final['AIcosts_s'] = data.iloc[:, 5]

#cols = ['sector', 'okved2', 'year', 'AIcosts_s']
#final = pd.DataFrame(final, columns=cols)

final = final[final['okved2'] != 'nan']

final = final.replace(to_replace='...', value=np.NAN)
final = final.replace(to_replace='…1)', value=np.NAN)
final = final.replace(to_replace='-', value=np.NAN)

final = final.astype({'AIcosts_s': 'float32', 'year': 'int32'})

final['AIcosts_s'] = final['AIcosts_s'] / 1000

data = pd.read_csv('AIcosts_s.csv')

data = pd.concat([data, final])

data.to_csv('AIcosts_s.csv', index=False)

print('done')