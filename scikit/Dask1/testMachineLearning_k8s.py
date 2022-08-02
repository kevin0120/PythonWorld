import time
from datetime import datetime

import dask
import numpy as np
from dask.distributed import Client, LocalCluster

import joblib
from sklearn.datasets import load_digits, load_wine

# -*- coding: utf-8 -*-

import os
from typing import Optional
from distutils.util import strtobool
from dask_gateway import Gateway, BasicAuth, GatewayCluster
from dask_gateway.client import ClusterStatus

glb_dask_gateway_cluster: Optional[GatewayCluster] = None

ENV_REMOTE_DASK_GATEWAY_ADDRESS = os.getenv('ENV_REMOTE_DASK_GATEWAY_ADDRESS',
                                            'http://42.192.175.212/services/dask-gateway')
ENV_DASK_GATEWAY_AUTH_USER = os.getenv('ENV_DASK_GATEWAY_AUTH_USER', 'admin')
ENV_DASK_GATEWAY_AUTH_PASSWORD = os.getenv('ENV_DASK_GATEWAY_AUTH_PASSWORD', '123456')


def _ensure_cluster(gateway: Gateway, address, username, password) -> GatewayCluster:
    _cluster_reports = gateway.list_clusters()
    if not _cluster_reports:
        _cluster = gateway.new_cluster(shutdown_on_close=False)
        return _cluster
    _active_cluster_name = ''
    for _cluster_report in _cluster_reports:
        if _cluster_report.status == ClusterStatus.RUNNING:
            _active_cluster_name = _cluster_report.name
            break
    if not _active_cluster_name:
        _active_cluster_name = _cluster_reports[0].name
    _cluster = GatewayCluster.from_name(_active_cluster_name, address=address,
                                        auth=BasicAuth(username=username, password=password))
    return _cluster


def get_dask_gateway_cluster() -> Optional[GatewayCluster]:
    global glb_dask_gateway_cluster
    if glb_dask_gateway_cluster:
        return glb_dask_gateway_cluster
    cluster = None
    if not check_remote_dask_cluster_enable():
        return cluster
    _gateway = Gateway(
        address=ENV_REMOTE_DASK_GATEWAY_ADDRESS,
        auth=BasicAuth(username=ENV_DASK_GATEWAY_AUTH_USER, password=ENV_DASK_GATEWAY_AUTH_PASSWORD)
    )
    cluster = _ensure_cluster(_gateway, ENV_REMOTE_DASK_GATEWAY_ADDRESS, ENV_DASK_GATEWAY_AUTH_USER,
                              ENV_DASK_GATEWAY_AUTH_PASSWORD)
    glb_dask_gateway_cluster = cluster
    return cluster


ENV_DASK_ENABLE = strtobool(os.getenv('ENV_DASK_ENABLE', 'false'))
ENV_DASK_MODE = os.getenv('ENV_DASK_MODE', 'LOCAL')  # LOCAL, REMOTE


def check_remote_dask_cluster_enable():
    return True


def check_local_dask_cluster_enable():
    return ENV_DASK_ENABLE and ENV_DASK_MODE in ['local', 'LOCAL']


if __name__ == '__main__':
    # client = Client(processes=False)  # create local cluster
    # client = Client(LocalCluster(n_workers=4, threads_per_worker=5, processes=True))
    # dask.config.set(scheduler='threads')
    # # # 1.分布式
    cluster = get_dask_gateway_cluster()
    cluster.scale(10)
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
    Xnew = [-6, -14] + [14, 18] * rng.rand(200000, 2)
    ynew = model.predict(Xnew)

    import dask.array as da

    d = da.from_array(Xnew, chunks=(5000, 2))
    # while True:
    #     for i in range(1000, 2000):
    #         b = datetime.now()
    #         predictions1 = model.predict(Xnew[:i + 1, ...])
    #         print("{}个数据本地用时{}ms".format(i + 1, (datetime.now() - b).microseconds / 1000))
    #         a = datetime.now()
    #
    #         # big_future = client.scatter(d[:i, ...])
    #         # L = client.submit(model.predict, big_future)
    #
    #         L = client.submit(model.predict, d[:i, ...])
    #         print(L.result())
    #         print("{}个数据dask用时{}ms".format(i + 1, (datetime.now() - a).microseconds / 1000))
    #         # L = client.submit(model.predict, X_test[:i, ...])
    #
    #         # print(client.gather(L))
    #         # total = client.submit(sum, L)
    #         # print(L.result())

    # while True:
    #     for i in range(100000, 200000):
    #         # with joblib.parallel_backend('dask'):
    #         # 根据练习集预测
    #         from datetime import datetime
    #         b = datetime.now()
    #         predictions1 = model.predict(Xnew[:i + 1, ...])
    #         print("{}个数据本地用时{}ms".format(i + 1, (datetime.now() - b).microseconds / 1000))
    #         a = datetime.now()
    #         predictions = model.predict(d[:i + 1, ...])
    #         print("{}个数据dask用时{}ms".format(i + 1, (datetime.now() - a).microseconds / 1000))
    #         time.sleep(5)
    #     time.sleep(3)

    # while True:
    #     for i in range(10000, 20000):
    #         # with joblib.parallel_backend('dask'):
    #         # 根据练习集预测
    #         from datetime import datetime
    #
    #         b = datetime.now()
    #         predictions1 = Xnew[:i + 1, ...].mean(axis=1)
    #         print("{}个数据本地用时{}ms".format(i + 1, (datetime.now() - b).microseconds / 1000))
    #         a = datetime.now()
    #         predictions = d[:i + 1, ...].mean(axis=1).compute()
    #         print("{}个数据dask用时{}ms".format(i + 1, (datetime.now() - a).microseconds / 1000))
    #         time.sleep(5)
    #     time.sleep(3)

    while True:
        for i in range(100000, 200000, 5):
            # with joblib.parallel_backend('dask'):
            # 根据练习集预测
            data = np.arange(i).reshape(int(i / 5), 5)
            from datetime import datetime

            b = datetime.now()

            bB1 = data.max(axis=1)[::-1]
            bB2 = data.max(axis=0)[::-1]
            bB3 = data.min(axis=1)[::-1]
            bB4 = data.min(axis=0)[::-1]

            print("{}个数据本地用时{}ms".format(i + 1, (datetime.now() - b).microseconds / 1000))
            a = datetime.now()

            f = da.from_array(data, chunks=(2500, 5))
            bB11 = f.max(axis=1)[::-1].compute()
            bB12 = f.max(axis=0)[::-1].compute()
            bB13 = f.min(axis=1)[::-1].compute()
            bB14 = f.min(axis=0)[::-1].compute()

            print("{}个数据dask用时{}ms".format(i + 1, (datetime.now() - a).microseconds / 1000))
            # time.sleep(5)
        time.sleep(3)
