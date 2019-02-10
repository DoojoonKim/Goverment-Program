# ex4_learning.py

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
import numpy as np
from time import time
from sklearn.metrics import accuracy_score


def ex4_learning():
    # 데이터를 준비한다.
    iris = datasets.load_iris()
    X = iris.data[:150, :]
    y = iris.target[:150]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 데이터 표준화를 통한 학습


    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    stime = time()
    ml = LogisticRegression(C=1000.0, random_state=0)
    ml.fit(X_train_std, y_train)
    etime = time()

    X_test_std = sc.transform(X_test)
    y_pred = ml.predict(X_test_std)


    # 차원 축소를 이용한 학습
    '''
    stime = time()
    pca1 = PCA(n_components=1)
    X_low = pca1.fit_transform(X_train)
    ml = LogisticRegression(C=1000.0, random_state=0)
    ml.fit(X_low, y_train)
    etime = time()

    pca2 = PCA(n_components=1)
    X_low2 = pca2.fit_transform(X_test)
    y_pred = ml.predict(X_low2)
    '''
    # 차원 축소를 하니 데이터가 손실이 되는 부분이 있다. 그래서 어쩔 수 없이 정확도가 떨어짐.
    # 그래서 속도를 선택하거나... 정확도를 선택하거나.. 둘 중 하나임.

    print("정확도 :", accuracy_score(y_test, y_pred))
    print("시간 :", (etime - stime))


