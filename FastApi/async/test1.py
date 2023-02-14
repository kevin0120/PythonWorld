import asyncio


async def func1():
    await asyncio.sleep(30)
    await func2()
    print('协程1')


async def func2():
    await asyncio.sleep(1)
    print('协程2')


# if __name__ == "__main__":
#     # task可为列表,即任务列表
#     # task = func1()
#     task = [func1(), func2()]
#     # 创建事件循环
#     loop = asyncio.get_event_loop()
#     # 添加任务，直至所有任务执行完成
#     loop.run_until_complete(asyncio.wait(task))
#     # 关闭事件循环
#     loop.close()

# python3.7引入的新特性，不用手动创建事件循环
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(5, 'hello')
    # await say_after(1, 'hello')执行完之后，才继续向下执行
    await say_after(10, 'world')

    print(f"finished at {time.strftime('%X')}")


if __name__ == "__main__":
    asyncio.run(main())
