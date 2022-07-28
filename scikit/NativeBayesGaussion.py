# https://blog.csdn.net/stillxjy/article/details/96153953
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns;

sns.set()

if __name__ == "__main__":
    from sklearn.datasets import make_blobs

    X, y = make_blobs(100, 2, centers=2, random_state=2, cluster_std=1.5)
    print(y)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='RdBu')
    plt.show()

    # 实例化高斯模型，并拟合数据：
    from sklearn.naive_bayes import GaussianNB

    model = GaussianNB()
    model.fit(X, y)

    # 生成测试数据，并预测：
    rng = np.random.RandomState(0)
    Xnew = [-6, -14] + [14, 18] * rng.rand(2000, 2)
    ynew = model.predict(Xnew)
    print(ynew)

    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='RdBu')
    lim = plt.axis()
    plt.show()
    plt.scatter(Xnew[:, 0], Xnew[:, 1], c=ynew, s=20, cmap='RdBu', alpha=0.1)
    plt.axis(lim)
    plt.show()
    yprob = model.predict_proba(Xnew)
    print(yprob[-8:].round(2))
