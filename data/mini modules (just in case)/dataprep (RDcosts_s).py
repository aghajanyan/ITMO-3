import csv
import numpy as np
import pandas as pd

def getsector(rawname):
    rawname = rawname.split('\n')
    rawname = rawname[1].split(' ', 1)
    return rawname[1]

def getsector(okved2, data):
    sector = ''
    for i in range(len(data)):
        if str(data.iloc[i, 1]).replace(' ', '') == okved2:
            sector = data.iloc[i, 0]
            break
    return sector
    

year = 2024
data = pd.read_excel(''+str(year)+'.xlsx', sheet_name=None)

tmp = []
final = []
for a in data.keys():
    tmp.append(getsector(data[a].columns[0]))
    tmp.append(a)
    tmp.append(year)
    tmp.append(data[a].iloc[4, 2])
    final.append(tmp)
    tmp = []

final = np.array(final)

cols = ['sector', 'okved2', 'year', 'RDcosts_s']
final = pd.DataFrame(final, columns=cols)

final = final.replace(to_replace='...', value=np.NAN)
final = final.replace(to_replace='-', value=np.NAN)

final['RDcosts_s'] = final['RDcosts_s'].astype(float)
final['RDcosts_s'] = final['RDcosts_s'] / 1000

final.to_csv(''+str(year)+'.csv', index=False)

print('done')