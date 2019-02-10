import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np
import collections

# 데이터를 읽어온다.
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# 데이터 시각화를 위한 함수
def bar_chart(feature) :
    # feature에 따라 생존한 사람을 카운트 한다.
    a1 = train[train['Survived'] == 1][feature].value_counts()
    # feature에 따라 사망한 사람을 카운트한다.
    a2 = train[train['Survived'] == 0][feature].value_counts()

    df = pd.DataFrame([a1, a2])
    df.index = ['Survive', 'Dead']
    df.plot(kind='bar', stacked=True, figsize=(10,5))
    plt.show()

import math

def check_nan(data, name) :
    count = 0
    for value in data[name] :
        if math.isnan(value) :
            count += 1
    print("nan :", count)


# bar_chart('Sex')
# bar_chart('Pclass')
# bar_chart('SibSp')
# bar_chart('Age')
# bar_chart('Fare')

# 1. 데이터 전처리
#  - 문자데이터를 수치화
#  - NaN(Null) 값을 어떻게 채워줄 것인가..
#    평균값으로 채워주거나 Null을 가지고 있는
#    로우를 날리거나...
#  - 기타 등등
# 데이터 전처리를 위해 학습데이터와 테스트데이터를
# 묶어서 관리하는 객체를 만든다.
train_test_data = [train, test]

# [이름 데이터 전처리]
# 이름 : 이름 자체는 별 의미가 없다.
# Mr, Mrs, MIss 등은 성별, 기혼여부를 파악할 수
# 있는 데이터이기 때문에 확인을 한다.
# 알파벳으로 시작해서 마침표(.)로 끝나는 단어를 추출
for dataset in train_test_data :
    dataset['Title'] = dataset['Name'].str.extract('([A-Za-z]+)\.', expand=False)

# print(train['Title'])
# print(train['Title'].value_counts())
# print(test['Title'].value_counts())
# bar_chart('Title')
title_mapping = {
    'Mr' : 0, 'Miss' : 1, 'Mrs' : 2,
    'Master' : 3, 'Dr' : 3, 'Rev' : 3,
    'Col' : 3, 'Mlle' : 3, 'Major' : 3,
    'Countess' : 3, 'Sir' : 3, 'Don' : 3,
    'Jonkheer' : 3, 'Lady' : 3, 'Capt' : 3,
    'Ms' : 3, 'Mme' : 3, 'Dona' : 3
}
for dataset in train_test_data :
    dataset['Title'] = dataset['Title'].map(title_mapping)
# print(dataset['Title'])

train.drop('Name', axis=1, inplace=True)
test.drop('Name', axis=1, inplace=True)

# [성별 데이터 전처리]
# male : 0, female : 1
sex_mapping = {'male' : 0, 'female' : 1}
for dataset in train_test_data :
    dataset['Sex'] = dataset['Sex'].map(sex_mapping)

# print(dataset['Sex'])

# [나이 데이터 전처리]
# Title 을 기준으로 평균 나이를 구해 채워준다.
train['Age'].fillna(train.groupby('Title')['Age'].transform('median'), inplace=True)
test['Age'].fillna(test.groupby('Title')['Age'].transform('median'), inplace=True)
# 나이를 그룹별로 묶어서 다시 셋팅한다.
# 16세 이하 : 0, 17 ~ 26 : 1, 27 ~ 36 : 2
# 37 ~ 62 : 3, 63세 이상 : 4
for dataset in train_test_data :
    dataset.loc[dataset['Age'] <= 16, 'Age'] = 0,
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 26), 'Age'] = 1,
    dataset.loc[(dataset['Age'] > 26) & (dataset['Age'] <= 36), 'Age'] = 2,
    dataset.loc[(dataset['Age'] > 36) & (dataset['Age'] <= 62), 'Age'] = 3,
    dataset.loc[dataset['Age'] > 62, 'Age'] = 4

# print(train['Age'])
# [가족 수]
# sibSp : 형제자매, Parch : 부모자식
train['FamilySize'] = train['SibSp'] + train['Parch'] + 1
test['FamilySize'] = test['SibSp'] + test['Parch'] + 1

family_mapping = {
    1:0, 2:0.4, 3:0.8, 4:1.2, 5:1.6, 6:2.0,
    7:2.4, 8:2.8, 9:3.2, 10:3.6, 11:4
}
for dataset in train_test_data :
    dataset['FamilySize'] = dataset['FamilySize'].map(family_mapping)

# bar_chart('FamilySize')
# [요금]
# nan 있는지 확인한다.
# check_nan(train, 'Fare')
# check_nan(test, 'Fare')
# bar_chart('Pclass')
test['Fare'].fillna(test.groupby('Pclass')['Fare'].transform('median'), inplace=True)

for dataset in train_test_data :
    dataset.loc[dataset['Fare'] <= 17, 'Fare'] = 0,
    dataset.loc[(dataset['Fare'] > 17) & (dataset['Fare'] <= 30), 'Fare'] = 1,
    dataset.loc[(dataset['Fare'] > 30) & (dataset['Fare'] <= 100), 'Fare'] = 2,
    dataset.loc[dataset['Fare'] > 100, 'Fare'] = 3

# bar_chart('Fare')
# [객실]
# bar_chart('Cabin')
# 첫 글자만 가지고 와서 교체해준다.
for dataset in train_test_data :
    dataset['Cabin'] = dataset['Cabin'].str[:1]
# print(train.Cabin.value_counts())
cabin_mapping = {
    'A' : 0, 'B' : 0.4, 'C' : 0.8, 'D' : 1.2,
    'E' : 1.6, 'F' : 2.0, 'G' : 2.4, 'T' : 2.8
}
for dataset in train_test_data :
    dataset['Cabin'] = dataset['Cabin'].map(cabin_mapping)
# nan 값 셋팅 : 각 등급별 구간 평균값을 넣어준다.
train['Cabin'].fillna(train.groupby('Pclass')['Cabin'].transform('median'), inplace=True)
test['Cabin'].fillna(test.groupby('Pclass')['Cabin'].transform('median'), inplace=True)
# bar_chart('Cabin')

#[선착장]
# bar_chart('Embarked')
# nan인 데이터는 S로 셋팅한다(S가 월등히 많아서..)
for dataset in train_test_data :
    dataset['Embarked'] = dataset['Embarked'].fillna('S')

embared_mapping = {'S' : 0, 'C' : 1, 'Q' : 2}
for dataset in train_test_data :
    dataset['Embarked'] = dataset['Embarked'].map(embared_mapping)

# 사용하지 않는 데이터 제거
drop_list = ['Ticket', 'SibSp', 'Parch']
train = train.drop(drop_list, axis=1)
test = test.drop(drop_list, axis=1)
train = train.drop(['PassengerId'], axis=1)
# 데이터를 분리한다.
target = train['Survived']
train_data = train.drop('Survived', axis=1)

# 2. 교차 검증을 통해 머신러닝 알고리즘을 선택
# 10개의 fold로 나눈다.
k_fold = KFold(n_splits=10, shuffle=True, random_state=0)
# 사용할 머신러닝 객체들을 만든다.
clf1 = KNeighborsClassifier(n_neighbors=13)
clf2 = DecisionTreeClassifier()
clf3 = RandomForestClassifier(n_estimators=13)
clf4 = GaussianNB()
clf5 = SVC(C=1, kernel='rbf', coef0=1)
clf6 = XGBClassifier()

# 교차 검증을 한다.
score1 = cross_val_score(clf1, train_data, target, cv=k_fold, n_jobs=1, scoring='accuracy')
score2 = cross_val_score(clf2, train_data, target, cv=k_fold, n_jobs=1, scoring='accuracy')
score3 = cross_val_score(clf3, train_data, target, cv=k_fold, n_jobs=1, scoring='accuracy')
score4 = cross_val_score(clf4, train_data, target, cv=k_fold, n_jobs=1, scoring='accuracy')
score5 = cross_val_score(clf5, train_data, target, cv=k_fold, n_jobs=1, scoring='accuracy')
score6 = cross_val_score(clf6, train_data, target, cv=k_fold, n_jobs=1, scoring='accuracy')

avg1 = round(np.mean(score1) * 100, 2)
avg2 = round(np.mean(score2) * 100, 2)
avg3 = round(np.mean(score3) * 100, 2)
avg4 = round(np.mean(score4) * 100, 2)
avg5 = round(np.mean(score5) * 100, 2)
avg6 = round(np.mean(score6) * 100, 2)
# 검증 수치를 출력한다.
print('kNN :', avg1)
print('Decision Tree :', avg2)
print('Random Forest :', avg3)
print('GaussianNB :', avg4)
print('SVM :', avg5)
print('XGBoost :', avg6)
# 3. 학습
# 제일 높게 나온 걸 이용하여 학습한다.
clf5.fit(train_data, target)
print("학습완료")
# 4. 써먹으면 됩니다~
test_data = test.drop('PassengerId', axis=1).copy()
y_pred = clf5.predict(test_data)

result = collections.Counter(y_pred)
print('사망 :', result[0])
print('생존 :', result[1])

# 결과 저장
submission = pd.DataFrame({
    'PassengerId' : test['PassengerId'],
    'Suvived' : y_pred
})
submission.to_csv('submission.csv')
print('결과 저장 완료')