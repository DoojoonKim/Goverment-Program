import numpy as np
from perceptron import Perceptron
from time import time
import pickle

def step1_learning() :
    # 학습과 테스트를 위해 사용할 데이터
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([-1, -1, -1, 1])
    # 퍼셉트론 객체를 생성한다.
    ppn = Perceptron(eta=0.1)
    #학습한다.
    stime = time()
    ppn.fit(X, y)
    etime = time()
    print("학습에 걸린 시간 :", (etime - stime))
    print("학습 중 오차가 난 개수 :", ppn.errors_)

    # 학습이 완료된 객체를 파일로 저장한다.
    with open('perceptron.dat', 'wb') as fp :
        pickle.dump(ppn, fp)

    print("머신러닝 학습 완료")

def step2_using() :
    # 파일로 부터 객체를 복원한다.
    with open('perceptron.dat', 'rb') as fp :
        ppn = pickle.load(fp)

    while True :
        a1 = input("첫 번째 2진수를 입력해주세요 :")
        a2 = input("두 번째 2진수를 입력해주세요 :")

        X = np.array([int(a1), int(a2)])
        # 계산된 결과를 가져온다.
        result = ppn.predict(X)
        if result == 1 :
            print("결과 : 1")
        else :
            print("결과 : 0")

# step1_learning()
step2_using()



# a1 = [1, 2]
# a2 = [3]
# a3 = zip(a1, a2)
# # zip 함수 : 앞===
# print(list(a3))

# a1 = [
#     [0,0],
#     [0,1],
#     [1,0],
#     [1,1]
# ]
# a2 = [0,0,0,1]
# a3 = zip(a1, a2)
# # 튜플로 프린트
# print(list(a3))