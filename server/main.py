import asyncio
import json
from lyrra import Lyrra
from lyrra.share.myLog import MyLog
from lyrra.control.userControl import UserControl
from lyrra.control.appControl import AppControl
from lyrra.control.gitlabControl import GitlabControl
from lyrra.share.myMysql import MyMysql
from lyrra.share.myExcept import MyException


class Main:
    app = Lyrra()

    @app.register("user")
    async def user(self, *args, **kwargs):
        userControl = UserControl()
        await UserControl.app.find(kwargs['data']['api'], kwargs['socket'], kwargs['data'])(userControl,
                                                                                            data=kwargs['data'],
                                                                                            socket=kwargs['socket'])
        return

    @app.register("app")
    async def appModel(self, *args, **kwargs):
        appControl = AppControl()
        await AppControl.app.find(kwargs['data']['api'], kwargs['socket'], kwargs['data'])(appControl,
                                                                                           data=kwargs['data'],
                                                                                           socket=kwargs['socket'])
        return

    @app.register("gitlab")
    async def gitlab(self, *args, **kwargs):
        gitlabControl = GitlabControl()
        await gitlabControl.app.find(kwargs['data']['api'], kwargs['socket'], kwargs['data'])(gitlabControl,
                                                                                              data=kwargs['data'],
                                                                                              socket=kwargs['socket'])
        return

    @Lyrra.checkoutDict
    @Lyrra.checkoutKv("model", "api")
    async def handle(self, *args, **kwargs):
        socket = kwargs['socket']
        data = kwargs['data']
        # 服务发现并执行
        await Main.app.find(data['model'], socket, data)(self, data=data, socket=socket)

    async def receive(self, reader, writer):
        data = await reader.readline()
        MyLog().logger.info(str(data))
        try:
            message = json.loads(data.decode('utf-8'))
        except Exception:
            ex = MyException(socket=writer)
            ex.reply('404')
        else:
            await self.handle(data=message, socket=writer)

        await writer.drain()
        writer.close()

    async def start(self):
        server = await asyncio.start_server(self.receive, '0.0.0.0', 8888)
        '''
        addr = server.sockets[0].getsockname()
        '''
        # 创建数据库池
        await MyMysql().getEn()
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    m = Main()
    asyncio.run(m.start())
