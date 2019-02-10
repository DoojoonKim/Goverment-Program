# ex7_LGBM.py
import numpy as np
from lightgbm import LGBMClassifier
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error


def ex7_LGBM():
    # 테스트할 데이터를 읽어온다. - 타이타닉 데이터
    X = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')

    # 학습 데이터와 테스트 데이터로 나눈다.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # lgbm = LGBMClassifier()
    lgbm = LGBMRegressor()
    lgbm.fit(X_train, y_train)

    y_pred = lgbm.predict(X_test)
    # print('정확도 :', accuracy_score(y_test, y_pred))
    print('정확도 :', 1 - mean_squared_error(y_test, y_pred))

