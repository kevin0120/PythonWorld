if __name__ == "__main__":
    # from dask.distributed import Client, progress
    #
    # client = Client(processes=False, threads_per_worker=4,
    #                 n_workers=1, memory_limit='2GB')
    # print(client)

    import dask.array as da

    x = da.random.random((10000, 10000), chunks=(1000, 1000))
    y = x + x.T
    z = y[::2, 5000:].mean(axis=1)
    z1 = z.compute()
    print(z.compute())

    import numpy as np;

    data = [1, 2, 3, 4, 5, 6]
    x1 = np.array(data)
    a = x1[::2]

    print("#################3")

    x = np.arange(16).reshape((4, 4))
    d = da.from_array(x, chunks=(2, 2))
    e = d.map_overlap(lambda x: x+ x.size, depth=1, boundary='reflect').compute()
    print(e)
