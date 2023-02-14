import asyncio
import time
from typing import Union

import uvicorn
from fastapi import FastAPI

app = FastAPI()


# //并发
@app.get("/async")
async def read_root():
    print("hello")
    await asyncio.sleep(10)
    print("world")
    return {"Hello": "World"}


# //并发
@app.get("/sync")
def read_root1():
    print("hello")
    time.sleep(10)
    print("world")
    return {"Hello": "World"}


# //非并发
@app.get("/sync2")
async def read_root2():
    print("hello")
    time.sleep(10)
    print("world")
    return {"Hello": "World"}


# //非并发
@app.get("/sync3")
async def read_root2():
    await rrr()
    return {"Hello": "World"}


async def rrr():
    print("hello")
    time.sleep(10)
    print("world")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


from fastapi.staticfiles import StaticFiles

# http://127.0.0.1:9900/static/test1.py
app.mount("/static", StaticFiles(directory="./async"), name="static")


def main(*args, **kwargs):
    uvicorn.run(app=app, host="0.0.0.0", port=9900)


if __name__ == "__main__":
    main()
