# ex1_basic.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def ex1_basic():
    a1 = ['calory', 'breakfast', 'lunch', 'dinner', 'exercise', 'body shape']
    df = pd.DataFrame(columns=a1)

    df.loc[0] = [1200, 1, 0, 0, 2, 'Skinny']
    df.loc[1] = [2800, 1, 1, 1, 1, 'Normal']
    df.loc[2] = [3500, 2, 2, 1, 0, 'Fat']
    df.loc[3] = [1400, 0, 1, 0, 3, 'Skinny']
    df.loc[4] = [5000, 2, 2, 2, 0, 'Fat']
    df.loc[5] = [1300, 0, 0, 1, 2, 'Skinny']
    df.loc[6] = [3000, 1, 0, 1, 1, 'Normal']
    df.loc[7] = [4000, 2, 2, 2, 0, 'Fat']
    df.loc[8] = [2600, 0, 2, 0, 0, 'Normal']
    df.loc[9] = [3000, 1, 2, 1, 1, 'Fat']
    # print(df)

    # 입력 데이터와 결과 데이터를 분리한다.
    a2 = ['calory', 'breakfast', 'lunch', 'dinner', 'exercise']
    a3 = ['body shape']
    X = df[a2]
    Y = df[a3]
    # print(X)
    # print(Y)

    # 수치가 굉장히 높은 calory 떄문에 전체 데이터를 표준화한다.
    st = StandardScaler()
    x_std = st.fit_transform(X)
    # print(x_std)

    # 공분산 행렬 : 공분산 값으로 이루어진 행렬
    # 공분산 값 : 좌표 성분들 값의 흩어진 정도가 얼마나 상관관계를 가지고 흩어져 있는지를 나타내는 값.
    features = x_std.T
    # 공분산 행렬
    covariance_matrix = np.cov(features)
    # print(covariance_matrix)

    # PC를 찾는다 ( 분산이 가장 넓은 지역 )
    eig_vals, eig_vecs = np.linalg.eig(covariance_matrix)
    # 5차원에서 1차원으로 변경시 정보 유실 확률 측정
    # print(1.0 - (eig_vals[0] / sum(eig_vals)))

    # 차원 축소
    projectd_X = x_std.dot(eig_vecs.T[0])
    # print(projectd_X)

    # DataFrame을 생성한다.
    result = pd.DataFrame(projectd_X, columns=['PC1'])
    # 시각화
    result['y-axis'] = 0.0
    result['label'] = Y
    # print(result)

    sns.lmplot('PC1', 'y-axis', result, fit_reg=False, scatter_kws={'s': 50}, hue='label')
    plt.title('PCA result')
    plt.show()
