import time

# http://www.devdoc.net/python/dask-2.23.0-doc/scheduling.html#
# http://www.devdoc.net/python/dask-2.23.0-doc/setup/single-distributed.html#
# http://127.0.0.1:8787/

if __name__ == "__main__":
    import dask.array as da
    import numpy as np
    import dask

    from dask.distributed import Client, LocalCluster

    # client = Client(LocalCluster(n_workers=3, threads_per_worker=7, processes=True))
    cluster = LocalCluster()
    client = Client(cluster)

    while True:
        for i in range(500, 1000):
            time.sleep(5)
            x = np.arange(i)
            print(x)
            y = da.from_array(x, chunks=205)
            # print(y)
            # print(y.mean())
            print(y.mean().compute())

            # 产生随机数:正态分布
            x = da.random.normal(0, 1, size=(100, 100), chunks=(88, 10))
            print(x.mean(axis=1).compute())
    # 3.

    # import dask.bag as db
    # b = db.from_sequence([1, 2, 3, 4, 5, 6])
    # print(b)
    # c = db.from_sequence([1, 2, 3, 4, 5, 6], npartitions=2)
    # print(c)
