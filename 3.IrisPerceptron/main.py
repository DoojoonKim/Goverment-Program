# Iris-setosa = 1
# Iris-versicolor = -1

import pandas as pd
import numpy as np
from perceptron import Perceptron
import pickle

def step1_get_data():
    # 1. iris.data 파일에서 데이터를 읽어온다.
    df = pd.read_csv('iris.data', header=None)
    # print(df)
    # 2. 꽃잎 데이터를 추출한다.
    # 0부터 100-1까지(100개), 2번 칼럼 3번 칼럼 추출
    X = df.iloc[0:100, [2, 3]].values
    # print(X)
    # 3. 꽃 종류 데이터를 추출한다.
    # 4번 칼럼 하나 추출
    y = df.iloc[0:100, 4].values
    # y 가 Iris-setosa면 1이고 다르면 -1로 바꿔라
    y = np.where(y=='Iris-setosa', 1, -1)
    # print(y)
    return X, y

def step2_learning():
    ppn = Perceptron(eta=0.1)

    # X, y 불러오기,,
    data = step1_get_data()
    # 파이썬에서 두 개 이상을 리턴하면 튜플로 나오기 때문에 0,1 로 구분해주는 것
    X = data[0]
    y = data[1]

    # 학습 시키기
    ppn.fit(X, y)

    print(ppn.errors_)
    # 가중치 프린트
    print(ppn.w_)
    # 학습된 객체를 저장한다.
    with open('perceptron.dat', 'wb') as fp :
        pickle.dump(ppn, fp)
    print("학습완료")
    

def step3_using() :
    # 파일로 부터 객체를 복원한다.
    with open('perceptron.dat', 'rb') as fp :
        ppn = pickle.load(fp)
    while True:
        a1 = input("너비를 입력해주세요.")
        a2 = input("길이를 입력해주세요.")

        X = np.array([float(a1), float(a2)])

        result = ppn.predict(X)
        if result == 1:
            print("결과 : 아이리스 세토사")
        else:
            print("결과 : 아이리스 벌시컬러")

# step1_get_data()
# step2_learning()
step3_using()

