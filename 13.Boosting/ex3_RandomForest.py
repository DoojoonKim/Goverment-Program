# ex3_RandomForest.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def ex3_RandomForest():
    # 테스트할 데이터를 읽어온다.
    X = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')

    # 학습 데이터와 테스트 데이터로 나눈다.
    # random_state 를 지정 안하면 실행할때마다 데이터를 랜덤하게 뽑아낸다. 값을 지정하면 일정하게 뽑혀나옴;
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 랜덤 포레스트를 만든다.
    eclf = RandomForestClassifier(oob_score=True)
    eclf.fit(X_train, y_train)

    y_pred = eclf.predict(X_test)
    print('정확도 :', accuracy_score(y_test, y_pred))


