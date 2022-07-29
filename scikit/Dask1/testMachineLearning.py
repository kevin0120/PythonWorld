import time

import numpy as np
from dask.distributed import Client, LocalCluster

import joblib
from sklearn.datasets import load_digits, load_wine

if __name__ == '__main__':
    # client = Client(processes=False)  # create local cluster
    client = Client(LocalCluster(n_workers=3, threads_per_worker=7, processes=False))

    # # 1.分布式
    # client = Client('127.0.0.1:8786')
    from sklearn.datasets import make_blobs

    X, y = make_blobs(100, 2, centers=2, random_state=2, cluster_std=1.5)
    # 实例化高斯模型，并拟合数据：
    from sklearn.naive_bayes import GaussianNB

    model = GaussianNB()
    model.fit(X, y)
    # print("参数w={},b={}".format(model.coef_, model.intercept_))
    # 生成测试数据，并预测：
    rng = np.random.RandomState(0)
    Xnew = [-6, -14] + [14, 18] * rng.rand(2000, 2)
    ynew = model.predict(Xnew)

    import dask.array as da

    d = da.from_array(Xnew, chunks=(1, 2))
    # while True:
    #     for i in range(1, 36):
    #         time.sleep(5)
    #         # L = client.submit(model.predict, X_test[:i, ...])
    #         L = client.submit(model.predict, d[:i, ...])
    #         # print(client.gather(L))
    #         # total = client.submit(sum, L)
    #         print(L.result())
    while True:
        for i in range(2000):
            # with joblib.parallel_backend('dask'):
            # 根据练习集预测
            predictions = model.predict(d[:i + 1, ...])
            print(predictions)
            time.sleep(3)
        time.sleep(3)
