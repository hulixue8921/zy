from lyrra import Lyrra
from lyrra.api.app import App
from lyrra.share.myExcept import MyException
import json
import jwt
import configparser


class AppControl:
    app = Lyrra()

    def __init__(self):
        self.app = App()

    @app.register("appAction")
    @Lyrra.checkoutKv("token", "fabuId", "type" , "projectName")
    @Lyrra.denyRedo(["fabuId", "type"])
    async def appAction(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}

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
            roleId = x['data']['roleId']
            fabus = await self.app.listFabu(roleId)
            for i in fabus:
                if data['fabuId'] == i['fabuId']:
                    gitAddress = await self.app.getGitAddressFromProjectName(data['projectName'])
                    sentData['message'] = await self.app.appAction(i['envName'], i['appName'],
                                                                   data['type'],gitAddress)
                    socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("fabu")
    @Lyrra.checkoutKv("token", "fabuId", "gitAddress", "gitCommit")
    @Lyrra.denyRedo(["fabuId"])
    async def fabu(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}

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
            roleId = x['data']['roleId']
            fabus = await self.app.listFabu(roleId)
            for i in fabus:
                if data['fabuId'] == i['fabuId']:
                    sentData['message'] = await self.app.fabu(i['envName'], i['appName'],
                                                              data['gitAddress'], data['gitCommit'])
                    socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("delApp")
    @Lyrra.checkoutKv("token", "appId")
    @Lyrra.checkoutRight("app::cms")
    async def delApp(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.app.delApp(data['appId']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register("addApp")
    @Lyrra.checkoutKv("token", "name", "git", "project")
    @Lyrra.checkoutRight("app::cms")
    async def addApp(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.app.addApp(data['name'], data['project'], data['git']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register("listApp")
    @Lyrra.checkoutKv("token")
    @Lyrra.checkoutRight("app::cms")
    async def listApp(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['app'] = await self.app.listApp()
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("listFabu")
    @Lyrra.checkoutKv("roleId")
    async def listFabu(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}

        sentData['fabu'] = await self.app.listFabu(data['roleId'])
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register('roleFabu')
    @Lyrra.checkoutKv("roleId", "fabuIds")
    async def roleFabu(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        await self.app.roleFabu(data['roleId'], data['fabuIds'])
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("listAppFabu")
    @Lyrra.checkoutKv("appId")
    async def listAppFabu(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['appFabu'] = await self.app.listAppFabu(data['appId'])
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register("listMyFabu")
    @Lyrra.checkoutKv("token")
    async def listMyFabu(self, *args, **kwargs):
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}

        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}

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
            roleId = x['data']['roleId']
            sentData['fabu'] = await self.app.listFabu(roleId)
            socket.write(json.dumps(sentData).encode('utf-8'))
