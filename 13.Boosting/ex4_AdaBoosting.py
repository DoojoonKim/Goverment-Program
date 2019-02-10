# ex4_AdaBoosting.py
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def ex4_AdaBoosting():
    # 테스트할 데이터를 읽어온다. - 타이타닉 데이터
    X = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')

    # 학습 데이터와 테스트 데이터로 나눈다.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 부스팅 시 사용될 머신러닝 알고리즘
    clf1 = DecisionTreeClassifier(max_depth=2)
    eclf = AdaBoostClassifier(base_estimator=clf1, n_estimators=500, learning_rate=0.1)
    # 학습한다.
    eclf.fit(X_train, y_train)
    # 정확도를 확인한다.
    y_pred = eclf.predict(X_test)
    print('정확도 :', accuracy_score(y_test, y_pred))
