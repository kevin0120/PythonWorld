import time

import numpy as np
from dask.distributed import Client, LocalCluster

import joblib
from sklearn.datasets import load_digits, load_wine

if __name__ == '__main__':
    # client = Client(processes=False)  # create local cluster
    cluster = LocalCluster()
    client = Client(cluster)
    # 加载数据
    X, y = load_wine(return_X_y=True)
    #
    # from sklearn.linear_model import LinearRegression
    # lr = LinearRegression()
    # Estimators（估算器）
    from sklearn.linear_model import LogisticRegression

    # from sklearn.naive_bayes import GaussianNB
    # 训练样本权重控制
    # https://blog.csdn.net/weixin_50304531/article/details/109717609
    # https://blog.csdn.net/qq_43391414/article/details/113144702
    lr = LogisticRegression(max_iter=10000, class_weight={0: 0.49, 1: 0.49, 2: 0.02})

    # 拆分数据集--训练+练习
    from sklearn.model_selection import train_test_split

    # test_size 联系集所占比例 random_state：是随机数的种子不填或者None每次都会不一样,填了每次都一样
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

    # 根据训练集练习模型
    import numpy as np

    # sample_weight 可以提高某一条数据的的权重
    aa = y_train.copy()
    aa[aa == 0] = 100
    model = lr.fit(X_train, y_train, sample_weight=aa)

    import dask.array as da
    d = da.from_array(X_test, chunks=(1, 13))
    # while True:
    #     for i in range(1, 36):
    #         time.sleep(5)
    #         # L = client.submit(model.predict, X_test[:i, ...])
    #         L = client.submit(model.predict, d[:i, ...])
    #         # print(client.gather(L))
    #         # total = client.submit(sum, L)
    #         print(L.result())
    while True:
        for i in range(1, 36):
            with joblib.parallel_backend('dask'):
                # 根据练习集预测
                predictions = model.predict(d[:i, ...])
                print(predictions)

                # # 模型评估 根据联系集预测
                # from sklearn.metrics import classification_report
                #
                # print(classification_report(y_test[:i], predictions))
            time.sleep(3)
        time.sleep(3)
