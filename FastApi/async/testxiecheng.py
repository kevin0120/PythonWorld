import time
import asyncio

async def func0(i):
    await asyncio.sleep(0.01)
    print('协程调用')
    return i


async def func1(i):
    time.sleep(0.01)
    print('协程调用')
    return i

async def func2(i):
    # get the event loop
    loop = asyncio.get_event_loop()
    # execute a function in a separate thread
    ret=  loop.run_in_executor(None, func1,i)
    return await ret



if __name__ == "__main__":
    # https://blog.csdn.net/qq_37674086/article/details/113884099

    # # 创建事件循环
    loop = asyncio.get_event_loop()
    bb = loop.run_until_complete(func2(100))
    cc = loop.run_until_complete(func0(111))
    dd = loop.run_until_complete(func1(123))

    # # # 阻塞运行
    # t1 = loop.time()
    # # 将协程转为task，并组成list
    # tasks = [asyncio.ensure_future(func1(i)) for i in range(100)]
    # aa = loop.run_until_complete(asyncio.gather(*tasks))
    # for done_task in aa:
    #     print((f"得到执行有序结果 {done_task}"))
    # t2 = loop.time()
    # print(t2-t1)

    # # # to_thread
    # t1 = loop.time()
    # # 将协程转为task，并组成list
    # tasks = [asyncio.ensure_future(func2(i)) for i in range(100)]
    # done= loop.run_until_complete(asyncio.gather(*tasks))
    # for done_task in done:
    #     print((f"得到执行无序结果 {done_task}"))
    # t2 = loop.time()
    # print(t2-t1)




    loop.run_forever()
    # 关闭事件循环
    loop.close()
