import asyncio
import json
import socket
import time

import aiomysql.sa.result

'''
x = {"model": "user", "api": "reg", "username": "胡", "passwd": "12345"}
y={"model": "k8s", "api": "reg"}

s = socket.socket()
s.connect(("localhost", 8888))
d=json.dumps(x)+"\n"
s.send(d.encode('utf-8'))

s1 = socket.socket()
s1.connect(("localhost", 8888))
t=json.dumps(y)+"\n"
s1.send(t.encode("utf-8"))
'''
from lyrra.share.myMysql import MyMysql
import asyncio


async def main():
    my = MyMysql()
    await my.getEn()
    await my.initData()


loop = asyncio.get_event_loop()

loop.run_until_complete(main())
