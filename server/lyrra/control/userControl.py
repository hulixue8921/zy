from lyrra import Lyrra
from lyrra.api.user import User
from lyrra.share.myExcept import MyException
import json


class UserControl:
    app = Lyrra()

    def __init__(self, *args, **kwargs):
        self.user = User()

    @app.register('reg')
    @Lyrra.checkoutKv("username", "passwd")
    async def reg(self, *args, **kwargs):
        """
        用户注册接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        try:
            judgment = await self.user.judgmentUser(data['username'])
            if judgment is False:
                x = await self.user.reg(data['username'], data['passwd'])
                if x:
                    socket.write(json.dumps(sentData).encode('utf-8'))
                else:
                    socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode('utf-8'))
            else:
                raise MyException(socket=socket)
        except MyException as e:
            e.reply('400')

    @app.register('load')
    @Lyrra.checkoutKv("username", "passwd")
    async def load(self, *args, **kwargs):
        """
        用户登录接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        try:
            judgment = await self.user.judgmentUserPasswd(data['username'], data['passwd'])
            if judgment is True:
                sentData['token'] = await self.user.getToken(data['username'], data['passwd'])
                sentData['mem'] = await self.user.getMem(data['username'], data['passwd'])
                socket.write(json.dumps(sentData).encode('utf-8'))
            else:
                raise MyException(socket=socket)
        except MyException as e:
            e.reply('401')

    @app.register('listUsers')
    @Lyrra.checkoutKv("token")
    @Lyrra.checkoutRight("admin")
    async def ListUsers(self, *args, **kwargs):
        """
        列出所有用户接口
        :param args: 不需要参数
        :param kwargs:不需要参数
        :return:'users'=[{id:"",username:"",roleId:"",roleName:""}]
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['users'] = await self.user.listUser()
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register('listRoles')
    @Lyrra.checkoutKv("token")
    @Lyrra.checkoutRight("admin")
    async def ListRoles(self, *args, **kwargs):
        """
        列出所有角色接口
        :param args:
        :param kwargs:
        :return: roles=[{roleId:"",roleName:""}]
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['roles'] = await self.user.listRoles()
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register('listMems')
    @Lyrra.checkoutKv("token")
    @Lyrra.checkoutRight("admin")
    async def listMems(self, *args, **kwargs):
        """
        列出所有菜单接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['mems'] = await self.user.listMems()
        socket.write(json.dumps(sentData).encode('utf-8'))

    @app.register('listRights')
    @Lyrra.checkoutKv("token")
    @Lyrra.checkoutRight("admin")
    async def listRights(self, *args, **kwargs):
        """
        列出超级管理员的权限
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['rights'] = await self.user.listRights()
        socket.write(json.dumps(sentData).encode("utf-8"))

    @app.register('delUser')
    @Lyrra.checkoutKv("token", "userId")
    @Lyrra.checkoutRight("admin")
    async def delUser(self, *args, **kwargs):
        """
        删除用户接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.delUser(data['userId']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode('utf-8'))

    @app.register('delRole')
    @Lyrra.checkoutKv("token", "roleId")
    @Lyrra.checkoutRight("admin")
    async def delRole(self, *args, **kwargs):
        """
        删除角色接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.delRole(data['roleId']):
            socket.write(json.dumps(sentData).encode("utf-8"))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register('delMem')
    @Lyrra.checkoutKv("token")
    @Lyrra.checkoutRight("admin")
    async def delMem(self, *args, **kwargs):
        pass

    @app.register('addRole')
    @Lyrra.checkoutKv("token", "roleName")
    @Lyrra.checkoutRight("admin")
    async def addRole(self, *args, **kwargs):
        """
        添加角色接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        await self.user.addRole(data['roleName'])
        socket.write(json.dumps(sentData).encode("utf-8"))

    @app.register('addMem')
    @Lyrra.checkoutKv("token", "memName")
    @Lyrra.checkoutRight("admin")
    async def addMem(self, *args, **kwargs):
        """
        添加菜单接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.addMem(data['memName']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register('userRole')
    @Lyrra.checkoutKv("token", "userId", "roleId")
    @Lyrra.checkoutRight("admin")
    async def userRole(self, *args, **kwargs):
        """
        修改用户角色接口
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.userRole(data['userId'], data['roleId']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register('roleRight')
    @Lyrra.checkoutKv("token", "roleId", "rightIds")
    @Lyrra.checkoutRight("admin")
    async def roleRight(self, *args, **kwargs):
        """
        修盖角色拥有某些权限
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.roleRights(data['roleId'], data['rightIds']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register('roleMem')
    @Lyrra.checkoutKv("token", "roleId", "memIds")
    @Lyrra.checkoutRight("admin")
    async def roleMem(self, *args, **kwargs):
        """
        修改角色拥有哪些菜单
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.roleMems(data['roleId'], data['memIds']):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register("updateUser")
    @Lyrra.checkoutKv("token", "userId", "roleId", "username")
    @Lyrra.checkoutRight("admin")
    async def updateUser(self, *args, **kwargs):
        """
        修改用户相关信息：修改用户名，用户角色id
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.updateUser(data['userId'], data['roleId'], data["username"]):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register("changePasswd")
    @Lyrra.checkoutKv("token", "userId", "passwd")
    @Lyrra.checkoutRight("admin")
    async def changePasswd(self, *args, **kwargs):
        """
        修改用户密码
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        if await self.user.changePasswd(data['userId'], data["passwd"]):
            socket.write(json.dumps(sentData).encode('utf-8'))
        else:
            socket.write(json.dumps({'code': 201, 'message': "未知错误"}).encode("utf-8"))

    @app.register("roleOwnMem")
    @Lyrra.checkoutKv("token", "roleId")
    @Lyrra.checkoutRight("admin")
    async def roleOwnMem(self, *args, **kwargs):
        """
        某角色所拥有的菜单项
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs['data']
        socket = kwargs['socket']
        sentData = {'code': 200}
        sentData['mems'] = await self.user.roleOwnMem(data['roleId'])
        socket.write(json.dumps(sentData).encode('utf-8'))
        pass
