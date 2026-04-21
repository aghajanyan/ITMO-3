import csv
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, f1_score, roc_curve
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


# получение датасета
data = pd.read_csv('classification prop 6.csv')
data = data.drop(columns=['sector', 'okved2', 'year', 'factoriescap_s','x' , 'y'])

data = data.sample(frac=1)  # перетасовка

# разбиение датасета на входные признаки и выходной результат (риск социального конфликта)
datasetin = np.array(data[data.columns.drop('clust')])
datasetout = np.array(data[['clust']])

# разбиение на обучающую и тестовую выборку
trainin, testin, trainout, testout = train_test_split(datasetin, datasetout, test_size=0.2, random_state=42)

# модель
model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(trainin, trainout.ravel())

predclass = model.predict(testin)
classerror = f1_score(testout.ravel(), predclass, average='macro')
print("f1 score: ", classerror)

#Корреляционная матрица Пирсона
cor = data.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

data = data[data.columns.drop('clust')]
# значимость факторов
plt.title("Значимость долевых значений признаков на прогноз кластера")
important = model.feature_importances_
forplot = pd.DataFrame(data=important, index=data.columns)
forplot = forplot.sort_values(by=[0])
plt.barh(forplot.index, forplot[0])
plt.xlabel("Importance score")
plt.ylabel("Feature")
plt.show()
