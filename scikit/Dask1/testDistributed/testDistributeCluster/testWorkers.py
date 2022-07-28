
if __name__ == "__main__":
    from dask.distributed import Client, Worker


    def inc(x):
        return x + 1


    import asyncio


    async def f(scheduler_address):
        w = await Worker(scheduler_address)
        await w.finished()


    asyncio.get_event_loop().run_until_complete(f("tcp://127.0.0.1:8786"))