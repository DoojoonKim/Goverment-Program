# ex3_face.py
from sklearn.datasets import fetch_olivetti_faces
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def show_image(images):
    N = 2
    M = 5
    fig = plt.figure(figsize=(10, 5))
    plt.subplots_adjust(top=1, bottom=0, hspace=0, wspace=0.05)
    for i in range(N):
        for j in range(M):
            k = i * M + j
            ax = fig.add_subplot(N, M, k+1)
            # ax.imshow(images[k], cmap=plt.cm.bone)
            ax.imshow(images[k].reshape(64, 64), cmap=plt.cm.bone)
            ax.grid(False)
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
    plt.suptitle('face picture')
    plt.tight_layout()
    plt.show()


def ex3_face():
    face_all = fetch_olivetti_faces()
    # faces = face_all.images[face_all.target == 9]
    faces = face_all.data[face_all.target == 9]
    # show_image(faces)

    # 차원 축소 - 2차원으로 축소
    pca1 = PCA(n_components=2)
    face_data = face_all.data[face_all.target == 9]
    W1 = pca1.fit_transform(face_data)
    # faces2 = pca1.inverse_transform(W1)
    # show_image(faces2)

    # 각 얼굴로부터 얻은 평준화된 데이터
    face_mean = pca1.mean_.reshape(64, 64)  # 사진 당 2개의 데이터가 있는데 그것을 합친 것.
    face_p1 = pca1.components_[0].reshape(64, 64)   # 1차원 데이터
    face_p2 = pca1.components_[1].reshape(64, 64)   # 2차원 데이터

    '''
    plt.subplot(131)
    plt.imshow(face_mean, cmap=plt.cm.bone)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.title("mean")

    # p1
    plt.subplot(132)
    plt.imshow(face_p1, cmap=plt.cm.bone)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.title("p1")

    # p2
    plt.subplot(133)
    plt.imshow(face_p2, cmap=plt.cm.bone)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.title("p2")
    
    plt.show()
    '''

    # 평균 얼굴에 주성분 1을 더한 사진
    N = 2
    M = 5
    fig = plt.figure(figsize=(10, 5))
    plt.subplots_adjust(top=1, bottom=0, hspace=0, wspace=0.05)
    for i in range(N):
        for j in range(M):
            k = i * M + j
            ax = fig.add_subplot(N, M, k + 1)
            w = k - 5 if k < 5 else k - 4
            ax.imshow(face_mean + w * face_p1, cmap=plt.cm.bone)
            ax.grid(False)
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])
    plt.suptitle('face picture')
    plt.tight_layout()
    plt.show()

