import csv
import numpy as np
import pandas as pd
import math

data = pd.read_excel('VDS_r.xlsx', sheet_name=6)

tmp = []
final = []

data = data.drop(data.index[0:3])
data = data.iloc[:-3]

region = 'Республика Казахстан'
i = 0
while i < data.shape[0]:
    if math.isnan(data.iloc[i, 2]):
        region = data.iloc[i, 1]
        i += 1
    else:
        try:
            year = data.iloc[i, 1].split(' ', 1)
            year = int(year[0])
            if year > 2000:
                tmp.append(region)
                tmp.append(year)
                # ВДС = ВРП - налоги
                tmp.append(float(data.iloc[i, 2]) - float(data.iloc[i, 24]))
                final.append(tmp)
                tmp = []
            i += 1
        except ValueError:
            i += 1

col = ['region', 'year', 'VDS_r']
final = pd.DataFrame(final, columns=col)

final = final.replace(to_replace='...', value=np.NAN)
final = final.replace(to_replace='…1)', value=np.NAN)
final = final.replace(to_replace='-', value=np.NAN)

final = final.astype({'VDS_r': 'float32'})

final = final.sort_values(by=['region', 'year'])
final = final.dropna()
final = final.reset_index(drop=True)

final.to_csv('VDS_r.kz-1.csv', index=False)

print('done')