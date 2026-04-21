import csv
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

#Наименьшие квадраты для одной переменной
def MLS(x, y):
    x = np.array(x).astype(float)
    y = np.array(y).astype(float)
    n = len(x)
    sumx, sumy = sum(x), sum(y)
    sumx2 = sum([t * t for t in x])
    sumxy = sum([t * u for t, u in zip(x, y)])
    a = (n * sumxy - (sumx * sumy)) / (n * sumx2 - sumx * sumx)
    b = (sumy - a * sumx) / n
    return a, b

datasetname = 'factoriescap_s (costs) 0 prop visnorm' # название датасета

# данные для нормализации (получение максимального значения factoriescap_s)
norm = pd.read_csv('../datasets/fornorm ' + datasetname + '.csv')
maxfactoriescap_s = norm.iloc[0]['factoriescap_s']

# получение датасета
data = pd.read_csv('../datasets/'+ datasetname +'.csv')
data = data.drop(columns=['sector', 'okved2', 'year'])

data = data.sample(frac=1)  # перетасовка

# разбиение датасета на входные признаки и выходной результат (риск социального конфликта)
datasetin = np.array(data[data.columns.drop('factoriescap_s')])
datasetout = np.array(data[['factoriescap_s']])

# разбиение на обучающую и тестовую выборку
trainin, testin, trainout, testout = train_test_split(datasetin, datasetout, test_size=0.2, random_state=42)

# модель
model = RandomForestRegressor(n_estimators=100, criterion='absolute_error', random_state=0)

model.fit(trainin, trainout.ravel())

predtrain = model.predict(trainin)
errortrain = r2_score(trainout * maxfactoriescap_s, predtrain * maxfactoriescap_s)

predtest = model.predict(testin)
errortest = r2_score(testout * maxfactoriescap_s, predtest * maxfactoriescap_s)

#a, b = MLS(testout, predtest)

print('R2 on training set: ', errortrain)
print('R2 on testing set: ', errortest)

# вывод отклонения прогноза от реальных значений
scale = np.linspace(trainout.min(), trainout.max(), 100)
plt.scatter(testout, predtest, c='black', alpha=.3, label='Testing set')
plt.plot([0,1], [0, 1], ls='--', c='red', label='Ideal')
plt.xlabel('Actual values')
plt.ylabel('Predictied values')
plt.legend()
plt.show()

#Корреляционная матрица Пирсона
cor = data.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

# значимость факторов
plt.title("Значимость признаков на прогноз factoriescap_s (объем производства собственных товаров, услуг итд")
data = data[data.columns.drop('factoriescap_s')]
important = model.feature_importances_

forplot = pd.DataFrame(data=important, index=data.columns)
forplot = forplot.sort_values(by=[0])
plt.barh(forplot.index, forplot[0])
plt.xlabel("Importance score")
plt.ylabel("Feature")
plt.show()
