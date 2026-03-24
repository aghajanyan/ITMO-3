import csv
import numpy as np
import pandas as pd

def getsector(rawname):
    rawname = rawname.split('\n')
    rawname = rawname[1].split(' ', 1)
    return rawname[1]


year = 2024
data = pd.read_excel(''+str(year)+'.xlsx', sheet_name=None)

sheets = data.keys()

tmp = []
final = []
for a in sheets:
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