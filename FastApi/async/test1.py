import time
import asyncio

 
# def callback(a, loop):
#     print("我的参数为 {0}，执行的时间为{1}".format(a,loop.time()))
 
 
# #call_later, call_at
# if __name__ == "__main__":
#     try:
#         loop = asyncio.get_event_loop()
#         now = loop.time()
#         loop.call_later(5, callback, 5, loop) #第一个参数设置的时间5.5秒后执行，
#         loop.call_at(now+2, callback, 2, loop)    #在指定的时间，运行，当前时间+2秒
#         loop.call_at(now+1, callback, 1, loop)
#         loop.call_at(now+3, callback, 3, loop)
#         loop.call_soon(callback, 4, loop)
#         loop.run_forever()  #要用这个run_forever运行，因为没有传入协程，这个函数在3.7中已经被取消
#     except KeyboardInterrupt:
#         print("Goodbye!")
 

async def func1():
    await asyncio.sleep(30)
    await func2()
    print('协程1')



async def func2():
    await asyncio.sleep(1)
    print('协程2')
    return 123

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
    # 添加任务，直至所有任务执行完成1
    # 将协程转为task，并组成list
    tasks = [
        asyncio.ensure_future(func2()),
        asyncio.ensure_future(func2()),
        asyncio.ensure_future(func2())
    ]
    aa= loop.run_until_complete(asyncio.gather(tasks))
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
