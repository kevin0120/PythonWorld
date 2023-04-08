import os

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn import metrics
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 加载数据
    x, y = make_blobs(n_samples=1000, n_features=4, centers=[[-1, -1, 6], [0, 0, 8], [1, 1, 9], [2, 2, 8]],
                      cluster_std=[0.4, 0.2, 0.2, 0.4], random_state=10)

    k_means = KMeans(n_clusters=3, random_state=10)

    k_means.fit(x)
    datapath = os.path.join("datasets", "lifesat", "")
    y_predict = k_means.predict(x)
    plt.scatter(x[:, 0], x[:, 1], c=y_predict)
    plt.show()
    print(k_means.predict((x[:30, :])))
    print(metrics.calinski_harabaz_score(x, y_predict))
    print(k_means.cluster_centers_)
    print(k_means.inertia_)
    print(metrics.silhouette_score(x, y_predict))
