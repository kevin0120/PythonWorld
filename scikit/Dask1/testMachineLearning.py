import time
from datetime import datetime

import dask
import numpy as np
from dask.distributed import Client, LocalCluster

import joblib
from sklearn.datasets import load_digits, load_wine

from scikit.Dask1.testMachineLearning_k8s import get_dask_gateway_cluster

if __name__ == '__main__':
    # client = Client(processes=False)  # create local cluster
    # client = Client(LocalCluster(n_workers=4, threads_per_worker=5, processes=True))
    # dask.config.set(scheduler='threads')
    # # 1.分布式
    cluster = get_dask_gateway_cluster()
    cluster.scale(1)
    client = cluster.get_client()
    from sklearn.datasets import make_blobs

    X, y = make_blobs(100, 2, centers=2, random_state=2, cluster_std=1.5)
    # 实例化高斯模型，并拟合数据：
    from sklearn.naive_bayes import GaussianNB

    model = GaussianNB()
    model.fit(X, y)
    # print("参数w={},b={}".format(model.coef_, model.intercept_))
    # 生成测试数据，并预测：
    rng = np.random.RandomState(0)
    Xnew = [-6, -14] + [14, 18] * rng.rand(20000000, 2)
    ynew = model.predict(Xnew)

    import dask.array as da

    d = da.from_array(Xnew, chunks=(500000, 2))
    # while True:
    #     for i in range(1, 36):
    #         time.sleep(5)
    #         # L = client.submit(model.predict, X_test[:i, ...])
    #         L = client.submit(model.predict, d[:i, ...])
    #         # print(client.gather(L))
    #         # total = client.submit(sum, L)
    #         print(L.result())
    while True:
        for i in range(10000000, 20000000):
            # with joblib.parallel_backend('dask'):
            # 根据练习集预测
            b = datetime.now()
            predictions1 = model.predict(Xnew[:i + 1, ...])
            print("{}个数据本地用时{}ms".format(i + 1, (datetime.now() - b).microseconds/1000))
            a = datetime.now()
            predictions = model.predict(d[:i + 1, ...])
            print("{}个数据dask用时{}ms".format(i + 1, (datetime.now() - a).microseconds/1000))
            # print(predictions)
            # yprob = model.predict_proba(d[:i + 1, ...])
            # print(yprob)
            time.sleep(5)
        time.sleep(3)
