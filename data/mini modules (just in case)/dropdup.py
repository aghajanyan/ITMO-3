import csv
import numpy as np
import pandas as pd

data = pd.read_csv('researchorg_s.csv')

data = data.drop_duplicates(subset=["sector", "year", "researchorg_s"], keep="last")
data = data.drop_duplicates(subset=["okved2", "year", "researchorg_s"], keep="last")
data = data.drop_duplicates(subset=["okved2", "year", "sector"], keep="last")
data = data.drop_duplicates()

data.to_csv('researchorg_s.csv', index=False)

print('done')