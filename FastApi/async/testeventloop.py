import time
import asyncio

async def func1():
    await asyncio.sleep(30)
    await func2()
    print('协程1')



async def func2(i=1):
    await asyncio.sleep(0.5)

    print('协程2')
    await asyncio.sleep(0.5)
    return i

if __name__ == "__main__":
    # https://blog.csdn.net/qq_37674086/article/details/113884099
    # task可为列表,即任务列表
    # task = func1()
    # task = [func1(), func2()]
    # # 创建事件循环
    # loop = asyncio.get_event_loop()
    # # 添加任务，直至所有任务执行完成1
    # loop.run_until_complete(asyncio.wait(task))
    # # 关闭事件循环
    # loop.close()

     # # 创建事件循环
    loop = asyncio.get_event_loop()
    t1 = loop.time()

    bb= loop.run_until_complete(func2(1999))
    # 添加任务，直至所有任务执行完成1
    # 将协程转为task，并组成list
    tasks = [asyncio.ensure_future(func2(i)) for i in range(100)]
    aa= loop.run_until_complete(asyncio.gather(*tasks))
    for done_task in aa:
        print((f"得到执行有序结果 {done_task}"))
    done, pending = loop.run_until_complete(asyncio.wait(tasks))
    for done_task in done:
        print((f"得到执行无序结果 {done_task.result()}"))
    t2 = loop.time()
    print(t2-t1)
    loop.run_forever()
    # 关闭事件循环
    loop.close()



    #  # 创建事件循环
    # loop = asyncio.get_event_loop()
    # # 添加任务，直至所有任务执行完成2
    # loop.run_until_complete(asyncio.gather(*task))
    # # 关闭事件循环
    # loop.close()

# # python3.7引入的新特性，不用手动创建事件循环


# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)


# async def main():
#     print(f"started at {time.strftime('%X')}")

#     await say_after(5, 'hello')
#     # await say_after(1, 'hello')执行完之后，才继续向下执行
#     await say_after(10, 'world')

#     print(f"finished at {time.strftime('%X')}")


# if __name__ == "__main__":
#     a = asyncio.get_event_loop()
#     asyncio.run(main())
