import csv
import math
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns

# медианное значение ВДС в кластере
def getmedian(data2):
    sns.boxplot(x='clust', y='VDS_s', data=data2, palette='viridis')

    plt.title("Медианное значение валовой добавленной стоимости в кластере")
    plt.xlabel('Cluster')
    plt.ylabel('ВДС')
    plt.show()


k = 4  # кол-во кластеров

data = pd.read_csv('../datasets/VDS_s.csv')
data = data.sample(frac=1)  # перетасовка

# модель кластеризации
clust_model = KMeans(n_clusters=k, random_state=None, n_init='auto')
clust_model.fit(data.iloc[:, 4:])  # 3 (без sector, ovked2, year и VDS)

# оценка модели и получение центроидов
print(clust_model.inertia_)
centroids = clust_model.cluster_centers_

# разметка данных согласно кластеру
data['clust'] = clust_model.labels_

# трансформация в 2D методом компонент
pca = PCA(2)
pca2 = pca.fit_transform(data.iloc[:, 4:])
data['x'] = pca2[:, 0]
data['y'] = pca2[:, 1]

# разделяем кластеры по независимым массивам (массив массивов)
clusts = []
for i in range(k):
    clusts.append(data[data['clust'] == i])

getmedian(data)

for i in range(k):
    plt.scatter(clusts[i]['x'], clusts[i]['y'], label="Cluster " + str(i) + "")

plt.title("Разбиение данных на " + str(k) + " кластера")
plt.xlabel('X')
plt.ylabel('Y')
plt.show()