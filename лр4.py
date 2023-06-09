# -*- coding: utf-8 -*-
"""mлр4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/182nfZTnMp2NnYuDAJZ4Qi95gAcB6wsLU

# Импорт данных
"""

import pandas as pd
import io
import numpy as np
import warnings

"""Загрузка данных в тетрадь"""

from google.colab import files
uploaded = files.upload()
dataset = pd.read_csv(io.BytesIO(uploaded['lr3-4.csv']), delimiter = ",")
df = pd.DataFrame(dataset)

"""Дан файл, содержащий сведения о посетителях фитнес-клуба. Описание колонок:
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

# Разработка предсказательной модели

Целевым признаком данной выборки является столбец churn - факт ухода из клуба.

Импортирование нужных модулей
"""

import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

"""Обязательная стандартизация данных перед работой с алгоритмами"""

scaler = StandardScaler() # создаем объект класса StandardScaler
scaler.fit(df.drop('churn',axis=1)) # Убираем целевой столбец и обучаем стандартизатор
scaled_features = scaler.transform(df.drop('churn',axis=1)) # Применить метод transform для стандартизации всех признаков
df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1])

"""Разделение на тестовый и тренажерный датасеты (x - датасет, y - значения churn)"""

x = df_feat
y = df['churn']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

"""## Балансирование классов"""

df['churn'].value_counts()

"""2939 человек остались в фитнес-клубе и 1061 ушли из него"""

count_no_sub = len(df[df['churn']==0])
count_sub = len(df[df['churn']==1])
pct_of_no_sub = count_no_sub/(count_no_sub+count_sub)
print("Процент оставшихся в клубе ", pct_of_no_sub*100)
pct_of_sub = count_sub/(count_no_sub+count_sub)
print("Процент ушедших из клуба ", pct_of_sub*100)

"""Классы не сбалансированы, и их соотношение составляет 73 к 27.

Выведем количество наблюдений каждого класса
"""

print(len(y_train))

print('Перед применением метода кол-во меток со значением True: {}'.format(sum(y_train == True)))
print('Перед применением метода кол-во меток со значением False: {}'.format(sum(y_train == False)))

"""Выполним балансировку данных"""

from imblearn.under_sampling import NearMiss
nm = NearMiss()
x_train, y_train = nm.fit_resample(x_train, y_train.ravel())

"""Выведем количество наблюдений каждого класса после балансировки"""

print('После применения метода кол-во меток со значением True: {}'.format(sum(y_train == True)))
print('После применения метода кол-во меток со значением False: {}'.format(sum(y_train == False)))

"""## Метод k- ближайших соседей"""

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1) # Создание экземпляра класса KNeighborsClassifier для k=1
knn.fit(x_train,y_train) # Обучение модели          
y_pred1 = knn.predict(x_test) # Предсказания модели

"""Выберем значение k по методу локтя"""

import matplotlib.pyplot as plt
error_rate = [] # Частота ошибок
for i in range(1,40):
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(x_train,y_train)
    pred_i = knn.predict(x_test)
    error_rate.append(np.mean(pred_i != y_test))

plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate, color='blue', linestyle='dashed', marker='o',markerfacecolor='red', markersize=10)
plt.xlabel('K')
plt.ylabel('Частота ошибок')
warnings.filterwarnings("ignore")

"""Из графика выше видно, что лучше использовать k = 19, т.к. оно имеет минимальную частоту ошибок."""

knn = KNeighborsClassifier(n_neighbors=19)
knn.fit(x_train,y_train)
y_pred1 = knn.predict(x_test)

"""#### Доля правильных ответов"""

from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred1)
print(acc)

"""84% правильных прогнозов.

#### Точность и полнота
"""

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
precision = precision_score (y_test, y_pred1)
recall = recall_score (y_test, y_pred1)
print(precision)
print(recall)

"""Точность и полнота близки к 1, следовательно классификация качественная.

#### Метрика "Balanced accuracy"
"""

from sklearn.metrics import balanced_accuracy_score
balanced_accuracy_score(y_test, y_pred1)

"""По этой метрике классификация является качественной.

#### F1-мера
"""

from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred1)
print(f1)

"""F1-мера близка к единице, следовательно классификация качественная.

#### Матрица ошибок
"""

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred1)
print(confusion_matrix)

"""Результат показывает, что 752 + 262 = 1013 верных прогнозов и 61 + 126 = 187 ошибочных.

## Логистическая регрессия
"""

from sklearn.linear_model import LogisticRegression
from sklearn import metrics
logreg = LogisticRegression()
logreg.fit(x_train, y_train)
y_pred2 = logreg.predict(x_test)

"""#### Доля правильных ответов"""

from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred2)
print(acc)

"""92% правильных прогнозов.

#### Точность и полнота
"""

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
precision = precision_score (y_test, y_pred2)
recall = recall_score (y_test, y_pred2)
print(precision)
print(recall)

"""Точность и полнота близки к 1, следовательно классификация качественная.

#### Метрика "Balanced accuracy"
"""

from sklearn.metrics import balanced_accuracy_score
balanced_accuracy_score(y_test, y_pred2)

"""По этой метрике классификация является качественной.

#### F1-мера
"""

from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred2)
print(f1)

"""F1-мера близка к единице, следовательно классификация качественная.

#### Матрица ошибок
"""

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred2)
print(confusion_matrix)

"""Результат показывает, что 832 + 268 = 1100 верных прогнозов и 46 + 54 = 100 ошибочных.

## Cлучайный лес
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)
y_pred3 = rfc.predict(x_test) # Предсказания модели

"""Вывод признаков по влиятельности"""

feats = {}
for feature, importance in zip(df.columns, rfc.feature_importances_):
    feats[feature] = importance
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-Importance'})
importances = importances.sort_values(by='Gini-Importance', ascending=False)
importances = importances.reset_index()
importances = importances.rename(columns={'index': 'Features'})
sns.set(font_scale = 5)
sns.set(style="whitegrid", color_codes=True, font_scale = 1.7)
fig, ax = plt.subplots()
fig.set_size_inches(30,15)
sns.barplot(x=importances['Gini-Importance'], y=importances['Features'], data=importances, color='skyblue')
plt.xlabel('Importance', fontsize=25, weight = 'bold')
plt.ylabel('Признаки', fontsize=25, weight = 'bold')
plt.title('Важность признака', fontsize=25, weight = 'bold')
display(plt.show())
display(importances)

"""Наибольшие влияние оказывает столбец lifetime - время с момента первого обращения в фитнес-центр

#### Доля правильных ответов
"""

from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred3)
print(acc)

"""90% правильных прогнозов.

#### Точность и полнота
"""

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
precision = precision_score (y_test, y_pred3)
recall = recall_score (y_test, y_pred3)
print(precision)
print(recall)

"""Точность и полнота близки к 1, следовательно классификация качественная.

#### Метрика "Balanced accuracy"
"""

from sklearn.metrics import balanced_accuracy_score
balanced_accuracy_score(y_test, y_pred3)

"""По этой метрике классификация является качественной.

#### F1-мера
"""

from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred3)
print(f1)

"""F1-мера близка к единице, следовательно классификация качественная.

#### Матрица ошибок
"""

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred3)
print(confusion_matrix)

"""Результат показывает, что 810 + 271 = 1081 верных прогнозов и 51 + 68 = 119 ошибочных.

## ROC-кривая
"""

warnings.filterwarnings("ignore")
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc1 = roc_auc_score(y_test, y_pred1)
fpr1, tpr1, thresholds1 = roc_curve(y_test, y_pred1)
logit_roc_auc2 = roc_auc_score(y_test, y_pred2)
fpr2, tpr2, thresholds2 = roc_curve(y_test, y_pred2)
logit_roc_auc3 = roc_auc_score(y_test, y_pred3)
fpr3, tpr3, thresholds3 = roc_curve(y_test, y_pred3)
plt.figure()

fig, ax = plt.subplots()
ax.plot(fpr1, tpr1, label = 'K-ближайших осседей')
ax.plot(fpr2, tpr2, label = 'Логистическая регрессия')
ax.plot(fpr3, tpr3, label = 'Случайный лес')

plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

"""Как видно из графика, метод логистическая регрессия является самым качественным из всех представленных в работе методов. Случайный лес показывает результат чуть похуже логистической регрессии.

# Вывод

Все использованные выше методы являются качественными для данного набора данных. Высокая доля правильных ответов у методов случайный лес и логистическая регрессия, 90 и 92 процента соответственно. А у метода k-ближайших соседей доля правильных ответов составляет 84%.
Точность и полнота ответов лучше выражена у метода логистическая регрессия. 
По всем метрикам, представленным выше, у метода логистической регрессии самые качественные прогнозы, а у метода k-ближайших соседей - наоборот.
"""