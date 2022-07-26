import asyncio
from aiohttp import web


async def hello(request):  # 创建请求处理程序
    await asyncio.sleep(0.5)
    text = '<h1>hello ,%s!</h1>' % (request.match_info['name'])
    # 这里的name是在init()里面注册的url里确定的
    # return web.Response(body=text.encode('utf-8'))#以特定编码返回要
    return web.Response(body=text.encode(), content_type='text/html')


async def index(request):
    return web.Response(body='<h1>Index</h1>'.encode(), content_type='text/html')


async def init(loop):
    app = web.Application()  # 创建application实例
    app.router.add_route('GET', '/', index)  # 注册路径与请求处理程序
    app.router.add_route('GET', '/hello/{name}', hello)  # 之所以上面能识别name，就是因为在这里定义的。
    srv = await loop.create_server(app._make_handler(), '127.0.0.1', 9000)
    print('server started at http://127.0.0.1:9000...')
    return srv


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
