# ex2_Bagging.py
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def ex2_Bagging():
   # 테스트할 데이터를 읽어온다. - 타이타닉 데이터
    X  = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')

    # 학습 데이터와 테스트 데이터로 나눈다.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 사용할 머신러닝 알고리즘 객체를 만든다.
    clf1 = DecisionTreeClassifier(random_state=1)
    # oob_score : 주어진 데이터셋을 통해 발생된 오차를 수정하기 위해 다른 데이터셋을 사용할 건지 여부
    eclf = BaggingClassifier(clf1, oob_score=True)
    # 학습한다.
    eclf.fit(X_train, y_train)

    y_pred = eclf.predict(X_test)
    print('정확도 : ', accuracy_score(y_test, y_pred))
