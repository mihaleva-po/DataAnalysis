# -*- coding: utf-8 -*-
"""mлр3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T1c56-heSLPHnVKFgyyGGvw134DB89Hd

# Импорт данных
"""

import pandas as pd
import io
import numpy as np

"""Загрузка данных в тетрадь"""

from google.colab import files
uploaded = files.upload()
dataset = pd.read_csv(io.BytesIO(uploaded['lr3.csv']), delimiter = ",")
df = pd.DataFrame(dataset)

"""Дан файл, содержащий сведения о заемщиках. Описание колонок:
1. gender: Пол, целочисленный тип
2. Near_Location: Близкое расположение, булевый тип
3. Partner: Сотрудник компании партнера, булевый тип
4. Promo_friends: По промо друзей, булевый тип
5. Phone: Указан ли телефон, булевый тип
6. Contract_period: Длительность текущего абонемента, целочисленный тип
7. Group_visits: Посещение групповых занятий, булевый тип
8. Age: Возраст, целочисленный тип
9. Avg_additional_charges_total: Средние траты на доп услуги, тип данных с плавающей запятой
10. Month_to_end_contract: Количество месяцев до окончания абонемента, целочисленный тип данных
11. Lifetime: время с момента первого обращения в фитнес-центр (в месяцах), целочисленный тип данных 
12. Avg_class_frequency_total: средняя частота посещений в неделю за все 
время с начала действия абонемента, тип данных с плавующей запятой
13. Avg_class_frequency_current_month: средняя частота посещений в неделю за 
предыдущий месяц, тип данных с плавующей запятой
14. Churn: факт ухода из клуба, булевый тип

Выведем 5 первых строчек файла
"""

df.head(5)

"""Посмотрим названия столбцов, типы данных и пропуски"""

df.info()

"""Имеются некорректные названия столбцов, т.е. названия начинаются с верхнего регистра. Изменим его на нижний."""

for Name, values in df.iteritems():
  df.rename(columns = {Name:Name.lower()}, inplace = True)

"""Проверим внесенные изменения"""

df.info()

"""Из информации выше видно, что пропуски отсутствуют. Тип данных некорректен у столбца month_to_end_contract. У столбцов "пол", "близкое расположение", "партнер", "по промо друзей", "групповые занятия" и "факт ухода из клуба" тип данных не будет изменён с целочисленного, на булевский, т.к. это помешает дальнейшему построению графиков.

# Проверка корректности значений данных

Проверим уникальные значения столбцов. Столбы gender, near_location, partner, promo_friends, phone, group_visits, churn должны содержать 0 или 1, в столбце Гендер 0 - женский пол, 1 - мужской. В остальных столбцах 0 - False, 1 - True.
Столбцы contract_period и month_to_end_contract должны содержать количество месяцев, т.е. целые положительные числа. Столбец lifetime содержит целочисленные значения не меньше 0. 
Столбец age - числа больше 0. 
Столбцы avg_additional_charges_total, avg_class_frequency_total и avg_class_frequency_current_month содержат данные с плавающей запятой не меньше 0.
"""

for name, values in df.iteritems():
  print(name)
  val = df[name].unique()
  val.sort()
  print(val)
  print('\n')

"""Все значения корректны, кроме типа данных столбца month_to_end_contract. Преобразуем его к целочисленному типу."""

df['month_to_end_contract'] = df['month_to_end_contract'].astype(int)

"""Проверим типы данных."""

print(df.dtypes)

"""Все типы данных корректны.

Проверим данные на наличие явных дубликатов.
"""

print(df.duplicated().sum())

"""Дубликаты данных отсутствуют.

# Кластеризация объектов иерархическим агломеративным методом

Импорт библиотек для выполнения кластеризации.
"""

import  sklearn
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage

"""С помощью метода linkage выполним иерархически агломеративную кластеризацию, в качестве метода подсчёта расстояний между объектами выбирается метод - ward (алгоритм минимизации дисперсии).

Обязательная стандартизация данных перед работой с алгоритмами
"""

scaler = StandardScaler() # создаём объект класса scaler
df = df.drop(columns = ["churn"]) # Убираем целевой столбец
scaler.fit(df) # обучаем стандартизатор
df_sc = scaler.transform(df) # преобразуем набор данных
linked = linkage(df_sc, method = 'ward')

"""Построим дендрограмму"""

plt.figure(figsize = (15,10))
dendrogram(linked,truncate_mode = "lastp")
plt.title('Hierarchial clustering for GYM')
plt.show()

"""Из дендограммы видно, что оптимальное число кластеров - 4. Также некоторые значения встречаются в нескольких кластерах, например, 139 есть в оранжевом и фиолетовом кластерах. Это говорит о том, что данные измерения находятся достаточно близко друг к другу, следовательно, по этим данным могут быть сделаны неправильные результаты, так как они могут относится как к одному классу предсказаний, так и к другому.

# Метод k-средних

Определим оптимальное количество кластеров
"""

from sklearn.cluster import KMeans

df_list = df.values.tolist()

inertia = []
for k in range(1, 8):
    kmeans = KMeans(n_clusters=k, random_state=1).fit(df_list)
    inertia.append(np.sqrt(kmeans.inertia_))

plt.plot(range(1, 8), inertia, marker='s');
plt.xlabel('$k$')
plt.ylabel('$J(C_k)$');

"""Видим, что J(C_k) падает сильно при увеличении числа кластеров с 1 до 4 и уже не так сильно – при изменении с 4 до 5. Значит, в данной задаче оптимально задать 4 кластера.

Создадим 4 кластера
"""

kmeans = KMeans(n_clusters=4, random_state=0) 
kmeans.fit(df_sc)

"""Выведем центроиды кластеров"""

cluster_center = kmeans.cluster_centers_
print(cluster_center)

"""Посмотрим метки для точек данных, т.е. к какому кластеру принадлежат данные"""

labels_4 = kmeans.labels_
print(labels_4.tolist())

"""Рассчитаем евклидово расстояние между кластерами."""

from scipy.spatial import distance
for i in range(len(cluster_center)):
  for j in range(len(cluster_center)):
    if j > i:
      print(f"Евклидово расстояние между группами {i} и {j} - ", distance.euclidean(cluster_center[i],cluster_center[j]))

"""# Метод k-средних для 2 кластеров

Создадим 2 кластера
"""

kmeans2 = KMeans(n_clusters=2, random_state=0) 
kmeans2.fit(df_list)

"""Выведем центроиды кластеров"""

cluster_center2 = kmeans.cluster_centers_
print(cluster_center2)

"""Посмотрим метки для точек данных"""

labels_2 = kmeans2.labels_
print(labels_2.tolist())

"""# Метрики силуэта для разных кластеров

Рассчитаем метрики силуэта для 4 и 2 кластеров.
"""

from sklearn.metrics import silhouette_score
silhouette_score(df_sc, labels_4)

silhouette_score(df_sc, labels_2)

"""Из данных выше видно, что при выделении 4 
кластеров метрика лучше, чем при 2х, но обе кластеризации являются некачественными (всего 13% и 6%).

# Признаки, оказавшие максимальное влияние на выделение кластеров

Распределяем все объекты по кластерам
"""

cluster_0 = []
cluster_1 = []
cluster_2 = []
cluster_3 = []
for i in range(len(labels_4)):
  if labels_4[i] == 0:
    cluster_0.append(df_sc[i])
  if labels_4[i] == 1:
    cluster_1.append(df_sc[i])
  if labels_4[i] == 2:
    cluster_2.append(df_sc[i])
  if labels_4[i] == 3:
    cluster_3.append(df_sc[i])
cluster_1[:5]

"""Для определения признаков, оказавших наибольшее влияние на выделение кластеров, находим Евклидовы расстояния между координатой центра и координатой точки каждого кластера."""

# Массив, хранящий евклидовы расстояния
dist = [[[] for i in range(13)] for k in range(4)]
def dis(cluster, cl): # cl - номер кластера
  for i in range(len(cluster)): # i - номер элемента кластера
    for j in range(13): # j - номер столбца
      dist[cl][j].append(distance.euclidean(cluster[i], cluster_center[cl][j]))
      dist[cl][j].sort()

dis(cluster_0, 0) 
dis(cluster_1, 1) 
dis(cluster_2, 2) 
dis(cluster_3, 3)    
print(dist)

"""Выведем евклидово расстояние и номер столбца, столбцы с наибольшим значением расстояния и будут самыми значимыми признаками."""

sred = [[[] for j in range(2)] for i in range(13)]
for i in range(13): # перебор координат
  ar = 0
  for k in range(4):
    ar += dist[k][i][-1]
  sred[i][0] = ar/4
  sred[i][1] = i+1
sred.sort(reverse=True)
print(sred)

"""Как видно из данных выше, наибольшее влияние на выделение кластеров оказали следующие столбцы: phone,contract_period month_to_end_contract.

# Вывод

Данные представляют набор сведений о посетителях фитнес центра с указанием их пола (gender), возраста (age), срока действия абонемента (contract_period), количестве трат на дополнительные услуги (additional_charges_total), количестве месяцев до окончания абонемента(month_to_end_contract), времени с момента первого посещения (time_since_first_visit), средней частоте посещений в неделю за всё время(class_frequency_total), средней частоте посещений в неделю за текущий месяц (class_frequency_current_month) и сведениями о том, живут ли они близко (near_location), являются ли сотрудниками фирм партнёров (partner), посещают ли они занятия по промо друзей (promo_friends), оставляли ли они свой телефон (phone), посещают ли они групповые занятия (group_visits).

Данные были стандартизированы и разделены на кластеры двумя методами: иерархическим агломеративным методом и методом k средних. Были выявлены признаки, которые оказали наибольшее влияние на выделение кластеров.

Исходя из обоих применённых методов разделения на кластеры, оптимальным количеством кластеров является 4. При этом метрика составляет около 13%, следовательно кластеризация не является качественной. Из дендрограммы видно, что некоторые значения присутствуют в разных кластерах, значит, разделение данных на кластеры неидеально. На выделение кластеров наибольшее влияние оказали следующие признаки: "Телефон", "Срок абонемента" и "Количество месяцев до окончания абонемента", т.е. столбцы phone,contract_period и month_to_end_contract.
"""