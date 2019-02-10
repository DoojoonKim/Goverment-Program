# perceptron.py
# Perceptron 알고리즘을 구현한 파일
import numpy as np

class Perceptron :
    # 생성자 함수 = 초기화 함수
    # thresholds : 임계값, 계산된 예측값을 비교하는 값
    # eta : 학습률
    # n_iter : 학습 횟수
    def __init__(self, thresholds=0.0, eta=0.01, n_iter=10):
        self.thresholds = thresholds
        self.eta = eta
        self.n_iter = n_iter

    # 학습 함수
    # X는 입력값, y는 결과값
    def fit(self, X, y):
        # 가중치를 담을 행렬을 생성한다. / 입력값이 2개니까 하나를 더 추가해놓은 것. 일단 0부터 출발
        self.w_ = np.zeros( 1 + X.shape[1])
        # 예츨값과 실제값을 비교하여
        # 다른 예측값의 갯수를 담을 리스트 (= 누적시킬 것임)
        self.errors_ = []

        # 지정된 학습 횟수만큼 반복한다.
        for _ in range(self.n_iter):
            # 예측값과 실제값이 다른 갯수를 담을 변수
            errors = 0
            # 입력받은 입력값과 결과값을 묶어 준다.
            temp1 = zip(X, y)
            # 입력값과 결과값 묶음을 가지고 반복한다. -> 학습 한 번 했다.
            for xi, target in temp1 :
                # 입력값을 가지고 예측값을 계산한다.
                a1 = self.predict(xi)
                # 입력값과 예측값이 다르면
                # 가중치를 계산한다.
                if target != a1 :
                    update = self.eta * (target - a1)
                    self.w_[1:] += update * xi
                    self.w_[0] += update
                    # 값이 다른 횟수를 누적한다.
                    errors += int(update != 0.0)

                # 값이 다른 횟수값을 배열에 담는다.
                self.errors_.append(errors)
                print(self.w_)



    # 가중치 * 이벽값의 총합을 계산
    # X는 입력값, y는 결과값
    def net_input(self, X):
        # 각 자리의 값과 가중치를 곱한 총합을 구한다. / 곱하기 연산 하나 덜 하려고 뒤에 하나 더한 것!
        a1 = np.dot(X, self.w_[1:]) + self.w_[0]
        return a1

    # 예측된 결과를 가지고 판단
    # X는 입력값, y는 결과값
    def predict(self, X):
        a2 = np.where(self.net_input(X) > self.thresholds, 1, -1)
        return a2


