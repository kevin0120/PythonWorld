import time

# dask-scheduler
# dask-worker tcp://127.0.0.1:8786


if __name__ == "__main__":
    from dask.distributed import Client

    def inc(x):
        return x + 1


    client = Client('127.0.0.1:8786')
    x1 = client.submit(inc, 10)
    print(x1.result())

    L = client.map(inc, range(1000))
    print(client.gather(L))
    total = client.submit(sum, L)
    print(total.result())
    # while True:
    #     time.sleep(0.1)
