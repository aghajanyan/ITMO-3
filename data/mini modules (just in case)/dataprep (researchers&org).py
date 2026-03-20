import csv
import numpy as np
import pandas as pd

# получение оквед2 из названия отрасли
def get_okved2(data):
    okved2 = []
    name = []
    for a in data:
        tmp = a.split('-')
        okved2.append(tmp[0][:-1])
        name.append(tmp[1].lstrip())
    return name, okved2

year = 2018

data = pd.read_excel(''+str(year)+'.xlsx')

data = data.drop(data.index[0:3])
data = data.iloc[:-2]   # удаление последних двух строк

name, okved2 = get_okved2(data.iloc[:,0])
data = data.drop(data.columns[0], axis=1)
data['sector'] = name
data['okved2'] = okved2

titles = ['researchersavg', 'org', 'sector', 'okved2']
data.columns = titles

x = data.iloc[7, 0]
data = data.replace(to_replace=x, value=np.NAN)

cols = ['sector', 'okved2', 'org', 'researchersavg']
data = data[cols]

data['year'] = year

data.to_csv(''+str(year)+'.csv', index=False)

print('done')