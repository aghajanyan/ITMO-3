import csv
import numpy as np
import pandas as pd


def getokved(rawname):
    rawname = rawname.split(' ')
    return rawname[1]

def getokato(region):
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

data = pd.read_excel('vds.xlsx', sheet_name='2.'+ str(year)+'')

data = data.drop(data.index[0:5])

tmp = []
final = []
for i in range(len(data)):
        reg, ok = getokato(data.iloc[i, 0])
        tmp.append(reg)
        tmp.append(ok)
        tmp.append(year)
        tmp.append(data.iloc[i, 1])
        final.append(tmp)
        tmp = []


final = np.array(final)

cols = ['region', 'okato', 'year', 'VDS_r']
final = pd.DataFrame(final, columns=cols)

final = final[final['okato'] != 'nan']

final = final.replace(to_replace='...', value=np.NAN)
final = final.replace(to_replace='…1)', value=np.NAN)
final = final.replace(to_replace='...1)', value=np.NAN)
final = final.replace(to_replace='-', value=np.NAN)

final = final.astype({'VDS_r': 'float32'})
final['VDS_r'] = final['VDS_r'] / 1000

final.to_csv(''+str(year)+'.csv', index=False)

print('done')