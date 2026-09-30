import csv
import numpy as np
import pandas as pd

regionname = 'г. Шымкент'


data = pd.read_excel(regionname+'.xlsx', sheet_name=0)

tmp = []
final = []

#data = data.drop(data.index[0:2])
#data = data.iloc[:-54]

year = int(data.columns[1])
for j in range(1, data.shape[1]):
    tmp.append(regionname)
    tmp.append(year)
    tmp.append(data.iloc[0, j])
    tmp.append(data.iloc[6, j])
    year+=1
    final.append(tmp)
    tmp = []


data = pd.read_excel(regionname+'.xlsx', sheet_name=1)

year = int(data.columns[1])
for j in range(1, data.shape[1]):
    tmp.append(regionname)
    tmp.append(year)
    tmp.append(data.iloc[0, j])
    tmp.append(data.iloc[8, j])
    year+=1
    final.append(tmp)
    tmp = []

data = pd.read_excel(regionname+'.xlsx', sheet_name=2)

year = int(data.columns[1])
for j in range(1, data.shape[1]):
    tmp.append(regionname)
    tmp.append(year)
    tmp.append(data.iloc[0, j])
    tmp.append(data.iloc[4, j])
    year+=1
    final.append(tmp)
    tmp = []


col = ['region', 'year', 'ITcosts_r', 'trainingcosts_r']
final = pd.DataFrame(final, columns=col)

final = final.replace(to_replace='-', value=np.NAN)
final = final.astype({'ITcosts_r': 'float32', 'trainingcosts_r': 'float32'}) # 'trainingcosts_r': 'float32'

if data.columns[0] == 'тыс. тенге':
    final['ITcosts_r'] = final['ITcosts_r'] / 1000
    final['trainingcosts_r'] = final['trainingcosts_r'] / 1000


final = final.sort_values(by=['region', 'year'])
final = final.reset_index(drop=True)

final.to_csv(regionname+'.csv', index=False)

print('done')