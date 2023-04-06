import time
import asyncio
import concurrent.futures as futures

async def func0(i):
    await asyncio.sleep(0.1)
    # print('协程调用')
    return i


def func01(i):
    time.sleep(0.1)
    # print('协程调用')
    return i


async def func1(i):
    time.sleep(0.1)
    # print('协程调用')
    return i


async def func2(i):
    # get the event loop
    loop = asyncio.get_event_loop()
    # execute a function in a separate thread
    ret = await loop.run_in_executor(None, func01, i)
    return ret

async def func3(i):
    # get the event loop
    loop = asyncio.get_event_loop()

    ex= futures.ThreadPoolExecutor(4) 
    ret = await loop.run_in_executor(ex, func01, i)
    return ret

async def func4(i):
    # get the event loop
    loop = asyncio.get_event_loop()

    ex= futures.ProcessPoolExecutor(2) 
    ret = await loop.run_in_executor(ex, func01, i)
    return ret

if __name__ == "__main__":
    # https://blog.csdn.net/qq_37674086/article/details/113884099

    # # 创建事件循环
    loop = asyncio.get_event_loop()

    # # 阻塞运行
    t1 = loop.time()
    # 将协程转为task，并组成list
    tasks = [asyncio.ensure_future(func1(i)) for i in range(100)]
    done = loop.run_until_complete(asyncio.gather(*tasks))
    print((f"得到执行有序序结果 {done}"))
    t2 = loop.time()
    print('运行一个异步函数func1 100次，但func1中有阻塞运行代码 耗时:', t2-t1)


    # # 原生的异步模块
    t1 = loop.time()
    # 将协程转为task，并组成list
    tasks = [asyncio.ensure_future(func0(i)) for i in range(100)]
    done = loop.run_until_complete(asyncio.gather(*tasks))
    print((f"得到执行有序序结果 {done}"))
    t2 = loop.time()
    print('运行一个异步函数func0 100次，func0中使用原生的异步模块asyncio.sleep耗时:', t2-t1)


    # # to_thread run_in_executor       ex= futures.ThreadPoolExecutor() 
    t1 = loop.time()
    # 将协程转为task，并组成list
    tasks = [asyncio.ensure_future(func3(i)) for i in range(100)]
    done = loop.run_until_complete(asyncio.gather(*tasks))
    print((f"得到执行有序序结果 {done}"))
    t2 = loop.time()
    print('运行一个异步函数func2 100次，func2中使用run_in_executor，并新建一个线程池ThreadPoolExecutor 运行阻塞代码耗时:', t2-t1)


    # # to_thread run_in_executor
    t1 = loop.time()
    # 将协程转为task，并组成list
    tasks = [asyncio.ensure_future(func2(i)) for i in range(100)]
    done = loop.run_until_complete(asyncio.gather(*tasks))
    print((f"得到执行有序序结果 {done}"))
    t2 = loop.time()
    print('运行一个异步函数func2 100次，func2中使用run_in_executor 运行阻塞代码耗时:', t2-t1)


    # # to_thread run_in_executor       ex= futures.ThreadPoolExecutor() 
    t1 = loop.time()
    # 将协程转为task，并组成list
    tasks = [asyncio.ensure_future(func4(i)) for i in range(100)]
    done = loop.run_until_complete(asyncio.gather(*tasks))
    print((f"得到执行有序序结果 {done}"))
    t2 = loop.time()
    print('运行一个异步函数func2 10次，func2中使用run_in_executor，并新建一个进程池ProcessPoolExecutor 运行阻塞代码耗时:', t2-t1)


    loop.run_forever()
    # 关闭事件循环
    loop.close()
