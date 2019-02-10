# ex5_GBM.py
import numpy as np
# Regressor -> 회귀라서 accuracy_score를 사용할 수 없음. (회귀 = 연속적인 데이터)
# Classifier -> 분류 -> 0, 1로 나눠서 하는 것.
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error



def ex5_GBM():
    # 테스트할 데이터를 읽어온다. - 타이타닉 데이터
    X = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')

    # 학습 데이터와 테스트 데이터로 나눈다.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # n_estimators : 최대 학습 개체의 갯수
    # max_depth : 최대 깊이 수
    # loss : 오차범위 수정을 위한 알고리즘. ls(기본), lad, huber, quantile
    # clf = GradientBoostingRegressor()
    clf = GradientBoostingRegressor(n_estimators=500, max_depth=2, loss='ls')
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    # accuracy_score로 하면 오류가 남.
    # print('정확도 :',  accuracy_score(y_test, y_pred))
    print('정확도 :', 1 - mean_squared_error(y_test, y_pred))

# 정확도 : 0.8534871052813966
