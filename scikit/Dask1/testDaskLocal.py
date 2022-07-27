# http://www.devdoc.net/python/dask-2.23.0-doc/setup/single-distributed.html
import time

import dask

if __name__ == "__main__":
    import dask.array as da
    import numpy as np

    # dask.config.set(scheduler='synchronous')
    # dask.config.set(scheduler='processes')This is the default scheduler for dask.bag
    # dask.config.set(scheduler='threads') This is the default scheduler for dask.array, dask.dataframe, and dask.delayed

    # dask.config.set(scheduler='processes')
    # 1.example----- HelloWorld
    x = np.arange(1000)
    print(x)
    y = da.from_array(x, chunks=205)
    # print(y)
    # print(y.mean())
    print(y.mean().compute(scheduler='processes'))

    # 产生随机数:
    x = da.random.normal(0, 1, size=(100, 100), chunks=(88, 10))
    print(x.mean().compute(scheduler='threads'))
    # 3.

    # import dask.bag as db
    # b = db.from_sequence([1, 2, 3, 4, 5, 6])
    # print(b)
    # c = db.from_sequence([1, 2, 3, 4, 5, 6], npartitions=2)
    # print(c)
    while True:
        time.sleep(0.1)
