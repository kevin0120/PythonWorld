import time

# dask-scheduler
# dask-worker tcp://127.0.0.1:8786

# https://docs.dask.org/en/latest/futures.html#distributed.Client
if __name__ == "__main__":
    from dask.distributed import Client, LocalCluster


    def inc(x):
        return x + 1


    # 1.分布式
    client = Client('127.0.0.1:8786')
    # # 2.local
    # cluster = LocalCluster()
    # client = Client(cluster)
    while True:
        for i in range(1000):
            time.sleep(5)
            x1 = client.submit(inc, i)
            print(x1.result())

            L = client.map(inc, range(i))
            print(client.gather(L))
            total = client.submit(sum, L)
            print(total.result())
