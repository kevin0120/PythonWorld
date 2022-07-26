from dask.distributed import Client

if __name__ == '__main__':
    client = Client("tcp://127.0.0.1:8786")
    a = client.map(lambda x: x ** 2, range(10))
    b = client.map(lambda x: x + 1, a)
    c = client.map(lambda x: -x, b)
    print(client.submit(sum, c).result)
