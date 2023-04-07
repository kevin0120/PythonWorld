import asyncio
import time
import queue
async def producer(q):
    data = input("请输入数据: ")
    while True:
        await asyncio.sleep(5)
        await q.put(data)
        print("producer:", data)
async def consumer(q):
    while True:
        # data = await q.get()
        data = await q.get()
        print("消费数据:", data)

async def main():
    q = asyncio.Queue()
    task1 = asyncio.create_task(producer(q))
    task2 = asyncio.create_task(consumer(q))
    await asyncio.gather(task1,task2)

asyncio.run(main())
if __name__ == "__main__":

    while True:
        time.sleep(1)
