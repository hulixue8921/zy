from lyrra import Lyrra
from lyrra.api.gitlab import Gitlab
from lyrra.share.myExcept import MyException
import json
import jwt
import configparser

class GitlabControl:
    app = Lyrra()

    def __init__(self):
        self.gitlab = Gitlab()

    @app.register("listProject")
    @Lyrra.checkoutKv("token")
    @Lyrra.denyRedo(["token"])
    async def listProject(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['project']=await self.gitlab.listProject()
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("listTag")
    @Lyrra.checkoutKv("gitProject")
    async def listTag(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['project'] = await self.gitlab.listTag(data['gitProject'])
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("listBranch")
    @Lyrra.checkoutKv("gitProject")
    async def listBranch(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['project'] = await self.gitlab.listBranch(data['gitProject'])
        socket.write(json.dumps(sentData).encode('utf-8'))
