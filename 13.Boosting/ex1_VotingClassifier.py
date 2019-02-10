# ex1_VotingClassifier.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris


def ex1_VotingClassifier():
    # 테스트할 데이터를 읽어온다. - 타이타닉 데이터
    X = np.load('./tatanic_X_train.npy')
    y = np.load('./tatanic_y_train.npy')
    # print(X)
    # print(y)

    # iris 데이터로 테스트 - 아이리스로도 보려고 한 것. 타이타닉으로 하려면 주석처리하면 됨.
    # iris = load_iris()
    # X = iris.data[:150, [2, 3]]
    # y = iris.target[:150]

    # 학습 데이터와 테스트 데이터로 나눈다.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # 예측에 사용될 모델들을 만든다.
    clf1 = LogisticRegression(random_state=1)
    clf2 = DecisionTreeClassifier(random_state=1)
    clf3 = GaussianNB()
    # 앙상블 모델을 만든다.
    a1 = [('lr', clf1), ('rf', clf2), ('gnb', clf3)]
    # voting : hard - 다수결 투표에 의해 결과를 선택
    #          soft - 예측 된 결과의 합계에 따라 선택
    eclf = VotingClassifier(estimators=a1, voting='hard')
    # 학습한다.
    eclf.fit(X_train, y_train)

    y_pred = eclf.predict(X_test)
    print('정확도 :', accuracy_score(y_test, y_pred))


