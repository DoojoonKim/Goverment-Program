# ex6_XGBoosting.py
import numpy as np
import sklearn.datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

def ex6_XGBoosting():
    # 테스트할 데이터를 읽어온다. - 타이타닉 데이터
    X = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')

    # 학습 데이터와 테스트 데이터로 나눈다.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # xgb = XGBClassifier()

    # n_jobs: 병렬처리로 사용할 쓰레드 개수를 정함. 정하지 않으면 default 값은 최댓값!
    # objective : 사용할 머신러닝 알고리즘 셋팅.
    #     기본은 reg:linear - linear regression
    #            reg:logistic - logistic regression
    #            binary:logistic - logistic regression for binary class
    #     http://xgboost-clone.readthedocs.io/en/latest/parameter.html
    # GPU -> 차원이 높은 데이터, 큰 데이터를 돌릴 때 유용.

    xgb = XGBRegressor()
    xgb.fit(X_train, y_train)

    y_pred = xgb.predict(X_test)
    # print('정확도 :', accuracy_score(y_test, y_pred))
    print('정확도 :', 1 - mean_squared_error(y_test, y_pred))