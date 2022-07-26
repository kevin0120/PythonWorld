import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.linear_model import LogisticRegression

if __name__ == "__main__":
    # 构造一些数据点
    centers = [[-5, 0], [0, 1.5], [5, -1]]
    X1, y = make_blobs(n_samples=1000, centers=centers, random_state=40)
    transformation = [[0.4, 0.2], [-0.4, 1.2]]
    X = np.dot(X1, transformation)

    clf = LogisticRegression(solver='sag', max_iter=100, random_state=42).fit(X, y)
    print(clf.coef_)
    print(clf.coef_.T)
    print(clf.intercept_)
    i = 1
    print(1 / (1 + np.exp(-(np.dot(X[i].reshape(1, -1), clf.coef_.T) + clf.intercept_))))
    print(y[i])
    print(X1[i])
    print(X[i])
    # print(clf.predict_proba(X[i].reshape(1, -1)))
    # print(clf.predict_log_proba(X[i].reshape(1, -1)))
