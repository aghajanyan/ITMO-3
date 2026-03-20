import csv
import numpy as np
import pandas as pd

year = 2024
finalorg = pd.DataFrame()
finalres = pd.DataFrame()
for k in range(7):
    data = pd.read_csv(''+str(year)+'.csv')
    year-= 1

    finalorg = pd.concat([finalorg, data])
    finalres = pd.concat([finalres, data])

finalorg = finalorg[finalorg.columns.drop('researchersavg')]
finalres = finalres[finalres.columns.drop('org')]

titles = ['sector', 'okved2', 'researchorg_s', 'year']
finalorg.columns = titles

cols = ['sector', 'okved2', 'year', 'researchorg_s']
finalorg = finalorg[cols]

titles = ['sector', 'okved2', 'researchersavg_s', 'year']
finalres.columns = titles

cols = ['sector', 'okved2', 'year', 'researchersavg_s']
finalres = finalres[cols]

finalorg = finalorg.sort_values(by=['okved2', 'year'])
finalres = finalres.sort_values(by=['okved2', 'year'])

finalorg.to_csv('researchorg_s.csv', index=False)
finalres.to_csv('researchersavg_s.csv', index=False)