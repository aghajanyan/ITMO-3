import csv
import math
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns

k = 4 # кол-во кластеров
datasetname = 'factoriescap_s (costs) 0' # название датасета

# медианное значение ключевого параметра в кластере
def getmedian(data2):
    sns.boxplot(x='clust', y='factoriescap_s', data=data2, palette='viridis')

    plt.title("Медианное значение объема собственного производства в кластере")
    plt.xlabel('Cluster')
    plt.ylabel('ВДС')
    plt.show()

# разделить кластер на нижний/верхний субкластер согласно медиане
def savesubcluster(clusts):
    norm = pd.read_csv('../datasets/fornorm '+ datasetname +'.csv')

    for a in range(len(clusts)):
        for col in norm:
            clusts[a][col] = clusts[a][col] * norm.iloc[0][col]

    final = []
    tmp = []
    for a in range(len(clusts)):
        for y in range(2):
            tmp.append(a)
            for col in norm:
                median = clusts[a][col].median()
                if y == 0:
                    subclust = clusts[a][clusts[a][col] < median][col].mean()
                else:
                    subclust = clusts[a][clusts[a][col] > median][col].mean()
                tmp.append(subclust)

            final.append(tmp)
            tmp = []

    final = np.array(final)
    features = list(norm.columns)
    features.insert(0, 'clust')
    final = pd.DataFrame(final, columns=features)
    final.to_excel(''+ str(k * 2) +' subclusters ('+datasetname+').xlsx', index=False)

# сохранить медианные значения каждого кластера для последующего анализа
def saveallmedians(clusts):
    norm = pd.read_csv('../datasets/fornorm '+ datasetname +'.csv')

    final = []
    tmp = []
    for a in range(len(clusts)):
        tmp.append(a)
        for col in norm:
            tmp.append(clusts[a][col].median() * norm.iloc[0][col])

        final.append(tmp)
        tmp = []

    final = np.array(final)
    features = list(norm.columns)
    features.insert(0, 'clust')
    final = pd.DataFrame(final, columns=features)
    final.to_excel('median of ' + str(k) + ' clusters (' + datasetname + ').xlsx', index=False)

# сохранить данные по всем кластерам в эксель файле в исходных значениях
def saveallclustersinseparatesheet(clusts):
    norm = pd.read_csv("../datasets/fornorm factoriescap_s (costs) 0.csv")

    writer = pd.ExcelWriter("Clusters factoriescap_s (costs) 0.xlsx")
    for a in range(len(clusts)):
        for col in norm:
            clusts[a][col] = clusts[a][col] * norm.iloc[0][col]

        clusts[a] = clusts[a].sort_values(by=['okved2', 'year'])
        clusts[a].to_excel(writer, sheet_name="Cluster " + str(a) + "", index=False)

    writer.close()

# сохранить данные по всем кластерам в эксель файле в исходных значениях
def saveallclustersinonesheet(data):
    norm = pd.read_csv('../datasets/fornorm '+ datasetname +'.csv')

    writer = pd.ExcelWriter('Clusters '+ str(k) +' '+ datasetname +'.xlsx')
    for col in norm:
        data[col] = data[col] * norm.iloc[0][col]

    data = data.drop(columns=['x', 'y'])
    data = data.sort_values(by=['okved2', 'year'])
    data = data.sort_values(by=['clust'])
    data.to_excel(writer, index=False)

    writer.close()

data = pd.read_csv('../datasets/'+ datasetname +'.csv')
data = data.sample(frac=1)  # перетасовка

# модель кластеризации
clust_model = KMeans(n_clusters=k, random_state=None, n_init='auto')
clust_model.fit(data.iloc[:, 4:])  # 3 (без sector, ovked2, year и key-indicator)

# оценка модели и получение центроидов
print(clust_model.inertia_)
centroids = clust_model.cluster_centers_

# трансформация в 2D методом компонент
pca = PCA(2)
pca2 = pca.fit_transform(data.iloc[:, 4:])
data['x'] = pca2[:, 0]
data['y'] = pca2[:, 1]

# разметка данных согласно кластеру
data['clust'] = clust_model.labels_

# разделяем кластеры по независимым массивам (массив массивов)
clusts = []
for i in range(k):
    clusts.append(data[data['clust'] == i])

# вывод графика с медианными значениями
getmedian(data)

# сохранить медианы кластеров в эксель
saveallmedians(clusts)

# сохраниить полные данные кластеров в эксель
saveallclustersinonesheet(data)

# сохранить субкластеры
savesubcluster(clusts)

# визуализация кластеризации
for i in range(k):
    plt.scatter(clusts[i]['x'], clusts[i]['y'], label="Cluster " + str(i) + "")

plt.title("Разбиение данных на " + str(k) + " кластера")
plt.xlabel('X')
plt.ylabel('Y')
plt.show()