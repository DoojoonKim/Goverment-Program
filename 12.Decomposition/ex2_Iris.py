# ex2_Iris.py
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA

def ex2_Iris():
    iris = load_iris()
    X = iris.data[:10, :2]
    '''
    plt.plot(X.T, 'o')
    plt.xticks(range(4), ['length', 'width'])
    plt.xlim(-0.5, 2)
    plt.ylim(2.5, 6)
    plt.title('attribute')
    plt.legend(['flower {}'.format(i+1) for i in range(10)])
    plt.show()
    '''
    # 차원축소
    pca1 = PCA(n_components=1)
    X_low = pca1.fit_transform(X)
    X2 = pca1.inverse_transform(X_low)

    plt.figure(figsize=(7, 7))
    ax = sns.scatterplot(0, 1, data=pd.DataFrame(X), s=100, color=".2", marker="s")
    for i in range(10):
        d = 0.03 if X[i, 1] > X2[i, 1] else -0.04
        ax.text(X[i, 0] - 0.065, X[i, 1] + d, "sample {}".format(i))
        plt.plot([X[i, 0], X2[i, 0]], [X[i, 1], X2[i, 1]], "k--")
    plt.plot(X2[:, 0], X2[:, 1], "o-", markersize=10)
    plt.plot(X[:, 0].mean(), X[:, 1].mean(), markersize=10, marker="D")
    plt.axvline(X[:, 0].mean(), c='r')
    plt.axhline(X[:, 1].mean(), c='r')
    plt.grid(False)
    plt.xlabel("length")
    plt.ylabel("width")
    plt.title("One-dimensional reduction")
    plt.axis("equal")
    plt.show()

    print(X2)
