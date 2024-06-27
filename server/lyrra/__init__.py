import asyncio

from lyrra.share.myExcept import MyException
from lyrra.share.myLog import MyLog
from lyrra.share.myMysql import MyMysql
from lyrra.share.myMem import MyMem
import json
import jwt
import configparser


class Lyrra:
    def __init__(self):
        # 注册用的
        self._dict = {}

    def register(self, name):
        def A(fun):
            self._dict[name] = fun

        return A

    def find(self, name, socket, data):
        try:
            if name is None:
                raise MyException(socket=socket)
            if name in self._dict:
                return self._dict[name]
            else:
                raise MyException(socket=socket)
        except MyException as e:
            e.reply('404')
            e.logError("数据格式不对，函数名没有注册：" + name)

            async def noUse(*args, **kwargs):
                pass

            return noUse

    @classmethod
    def checkoutDict(cls, fun):
        async def A(*args, **kwargs):
            try:
                if isinstance(kwargs['data'], dict):
                    await fun(*args, **kwargs)
                else:
                    raise MyException(socket=kwargs['socket'])
            except MyException as e:
                e.reply('404')
                e.logError("数据格式不对，不是字典：" + json.dumps(kwargs['data']))

        return A

    @classmethod
    def checkoutKv(cls, *keys):
        def A(fun):
            async def B(*args, **kwargs):
                x = 0
                for key in keys:
                    if key in kwargs['data'].keys():
                        if kwargs['data'][key] or isinstance(kwargs['data'][key], list):
                            x = x + 1
                try:
                    if x == len(keys):
                        try:
                            await fun(*args, **kwargs)
                        except Exception:
                            myEx = MyException(socket=kwargs['socket'])
                            myEx.reply('500')
                    else:
                        raise MyException(socket=kwargs['socket'])
                except MyException as e:
                    e.reply('404')
                    e.logError("数据格式不对，缺少必要参数" + json.dumps(kwargs['data']))

            return B

        return A

    @classmethod
    def checkoutRight(cls, key):
        right = key

        def A(fun):
            async def B(*args, **kwargs):
                data = kwargs['data']
                socket = kwargs['socket']

                config = configparser.ConfigParser()
                config.read('./etc/config.ini')
                iss = config['token']['iss']
                key1 = config['token']['key']
                algo = config['token']['algo']
                try:
                    x = jwt.decode(data['token'], key1, issuer=iss, algorithms=[algo])
                except Exception:
                    myEx = MyException(socket=socket)
                    myEx.reply('402')
                else:
                    checkRights = x['data']['right']
                    if right in checkRights:
                        await fun(*args, **kwargs)
                    else:
                        myEx = MyException(socket=socket)
                        myEx.reply('403')

            return B

        return A

    @classmethod
    def denyRedo(cls, keys):
        def A(fun):
            async def B(*args, **kwargs):
                data = kwargs['data']
                socket = kwargs['socket']
                funName = fun.__name__
                funClassName = fun.__qualname__
                judgment = funName + funClassName

                for i in keys:
                    judgment = judgment + "-" + i + "-" + str(data[i])

                mem = MyMem()
                if await mem.judementKey(judgment):
                    try:
                        raise MyException(socket=socket)
                    except MyException as e:
                        e.reply('405')
                else:
                    await mem.set(judgment, 1)
                    await fun(*args, **kwargs)
                    await mem.delKey(judgment)

            return B

        return A
