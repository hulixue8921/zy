import asyncio

globalDict = {}


def wapper(cls):
    def A(*args, **kwargs):
        if cls not in globalDict:
            globalDict[cls] = cls(*args, **kwargs)
        return globalDict[cls]

    return A


@wapper
class MyMem:
    def __init__(self):
        self._dist={}

    async def get(self, key):
        return self._dist[key]

    async def set(self, key , value):
        self._dist[key]=value

    async def delKey(self, key):
        self._dist.pop(key)

    async def judementKey(self, key):
        if key in self._dist:
            return True
        else:
            return False
