from lyrra import Lyrra
from lyrra.share.myMysql import MyMysql
from lyrra.share.myTable import MyTable
import configparser
import time
import jwt
import sqlalchemy as sa
from sqlalchemy import or_


def memDataHandle(listData, container):
    """
    :param listData:
    :param container:
    :return:
    将菜单数据转成树形结构
    """
    dataTemp = []

    def handle(mylist: list, container1: dict) -> dict:
        if len(mylist) == 0:
            return
        else:
            x = mylist.pop(0)
            if x in container1:
                handle(mylist, container1[x])
            else:
                if len(mylist) == 0:
                    container1[x] = {}
                else:
                    y = mylist.pop(0)
                    container1[x] = handle1(y, mylist)

    def handle1(a, b):
        if len(b) == 0:
            temp = {}
            temp[a] = {}
            return temp
        else:
            x = b.pop(0)
            temp = {}
            r = handle1(x, b)
            temp[a] = r
            return temp

    handle(listData, container)
    return


class User:
    app = Lyrra()

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./etc/config.ini')
        self.iss = config['token']['iss']
        self.key = config['token']['key']
        self.algo = config['token']['algo']
        self.tokenTimeout = int(config['token']['timeout'])
        self.mysql = MyMysql()
        self.tables = MyTable()

    async def judgmentUser(self, username):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_user.c.username
                ).where(
                    self.tables.t_user.c.username == username
                )
            )
            result = await proxy.fetchone()
            await trans.commit()
            if result is not None:
                return True
            else:
                return False

    async def judgmentUserPasswd(self, username, passwd):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_user.c.username
                ).where(
                    self.tables.t_user.c.username == username
                ).where(
                    self.tables.t_user.c.passwd == passwd
                )
            )
            result = await proxy.fetchone()
            await trans.commit()
            if result is not None:
                return True
            else:
                return False

    async def reg(self, username, passwd):
        """
        新用户都给分配个匿名角色
        """
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(
                    sa.insert(
                        self.tables.t_user
                    ).values(
                        username=username, passwd=passwd)
                )

                idProxy = await conn.execute("SELECT LAST_INSERT_ID()")
                id = await idProxy.fetchone()
                id = id[0]

                roleProxy = await conn.execute(
                    sa.select(
                        self.tables.t_role.c.id
                    ).where(
                        self.tables.t_role.c.name == "匿名角色"
                    )
                )
                rid = await roleProxy.fetchone()
                rid = rid[0]
                await conn.execute(
                    sa.update(
                        self.tables.t_user
                    ).values(
                        roleId=rid
                    ).where(
                        self.tables.t_user.c.id == id
                    )
                )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def getToken(self, username, passwd):
        d = {}
        data = {
            'right': await self.getRight(username, passwd),
            'username': username,
            'passwd': passwd,
            'roleId': await self.getRoleId(username)
        }
        d['data'] = data
        d['exp'] = time.time() + self.tokenTimeout
        d['iss'] = self.iss
        return jwt.encode(d, self.key, algorithm=self.algo)

    async def getRoleId(self, username):
        mysqlEn = await self.mysql.getEn()
        data = None
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(self.tables.t_user.c.roleId).where(self.tables.t_user.c.username == username)
            )
            roleId = await proxy.fetchone()
            data = roleId[0]
            await trans.commit()
        return data

    async def getRight(self, username, passwd):
        mysqlEn = await self.mysql.getEn()
        data = []
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_right.c.value
                ).where(
                    self.tables.t_user.c.roleId == self.tables.t_role.c.id
                ).where(
                    self.tables.t_role.c.id == self.tables.t_role_right.c.roleId
                ).where(
                    self.tables.t_role_right.c.rightId == self.tables.t_right.c.id
                ).where(
                    self.tables.t_user.c.username == username, self.tables.t_user.c.passwd == passwd
                )

            )
            async for i in proxy:
                data.append(i[0])
            await trans.commit()
        return data

    async def getMem(self, username, passwd):
        mysqlEn = await self.mysql.getEn()
        data = {}
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_mem.c.value
                ).where(
                    self.tables.t_user.c.roleId == self.tables.t_role.c.id
                ).where(
                    self.tables.t_role.c.id == self.tables.t_role_mem.c.roleId
                ).where(
                    self.tables.t_role_mem.c.memId == self.tables.t_mem.c.id
                ).where(
                    self.tables.t_user.c.username == username, self.tables.t_user.c.passwd == passwd
                )
            )
            await trans.commit()
            async for x in proxy:
                listTemp = []
                for i in x[0].split(":"):
                    listTemp.append(i)
                memDataHandle(listTemp, data)
        return data

    async def listUser(self, *args, **kwargs):
        mysqlEn = await self.mysql.getEn()
        data = []
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_user.c.id, self.tables.t_user.c.username, self.tables.t_user.c.roleId,
                    self.tables.t_role.c.name
                ).where(
                    self.tables.t_user.c.username != 'root'
                ).where(
                    self.tables.t_user.c.roleId == self.tables.t_role.c.id
                )
            )
            async for i in proxy:
                data.append({'id': i[0], 'username': i[1], 'roleId': i[2], 'roleName': i[3]})
            await trans.commit()
        return data

    async def listRoles(self, *args, **kwargs):
        mysqlEn = await self.mysql.getEn()
        data = []
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_role.c.id, self.tables.t_role.c.name
                )
            )
            async for i in proxy:
                data.append({'roleId': i[0], 'roleName': i[1]})
            await trans.commit()
        return data

    async def listMems(self, *args, **kwargs):
        mysqlEn = await self.mysql.getEn()
        data = []
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(
                    self.tables.t_mem.c.id, self.tables.t_mem.c.value
                )
            )
            async for i in proxy:
                data.append({'memId': i[0], 'memValue': i[1]})
            await trans.commit()
        return data

    async def listRights(self, *args, **kwargs):
        mysqlEn = await self.mysql.getEn()
        data = []
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            proxy = await conn.execute(
                sa.select(self.tables.t_right.c.id, self.tables.t_right.c.name, self.tables.t_right.c.value)
            )

            async for i in proxy:
                data.append({"id": i[0], "name": i[1], "value": i[2]})
            await trans.commit()
        return data

    async def delUser(self, userId):
        """
        管理员用户不允许被删除
        :param userId:
        :return:
        """
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_user.c.id).where(self.tables.t_user.c.username == "root"))
                rootId = await proxy.fetchone()
                rootId = rootId[0]
                if userId == rootId:
                    raise Exception

                await conn.execute(
                    sa.delete(
                        self.tables.t_user
                    ).where(
                        self.tables.t_user.c.id == userId
                    )
                )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def delRole(self, roleId):
        """
        删除的角色所关联的用户，将给予匿名用户角色
        管理员角色 or 匿名角色不允许被删除
        :param roleId:
        :return:
        """
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_role.c.id).where(
                        or_(self.tables.t_role.c.name == "管理员", self.tables.t_role.c.name == "匿名角色"))
                )
                ids = []
                async for id in proxy:
                    ids.append(id[0])

                if int(roleId) in ids:
                    raise Exception

                lambdaRoleIdProxy = await conn.execute(
                    sa.select(self.tables.t_role.c.id).where(self.tables.t_role.c.name == "匿名角色")
                )
                lambdaRoleId = await lambdaRoleIdProxy.fetchone()
                lambdaRoleId = lambdaRoleId[0]
                await conn.execute(
                    sa.delete(
                        self.tables.t_role
                    ).where(
                        self.tables.t_role.c.id == roleId
                    )
                )
                await conn.execute(
                    sa.update(
                        self.tables.t_user
                    ).values(
                        roleId=lambdaRoleId
                    ).where(self.tables.t_user.c.roleId == roleId)
                )
                await conn.execute(
                    sa.delete(self.tables.t_role_mem).where(self.tables.t_role_mem.c.roleId == roleId)
                )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def addRole(self, roleName):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(sa.insert(self.tables.t_role).values(name=roleName))
            except Exception:
                await trans.rollback()
            else:
                await trans.commit()

    async def addMem(self, memValue):
        """
        添加的菜单，会自动分配给管理员角色
        :param memValue:
        :return:
        """
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(
                    sa.insert(self.tables.t_mem).values(value=memValue)
                )
                memProxy = await conn.execute("SELECT LAST_INSERT_ID()")
                memId = await memProxy.fetchone()
                memId = memId[0]
                roleProxy = await conn.execute(
                    sa.select(
                        self.tables.t_role.c.id
                    ).where(
                        self.tables.t_role.c.name == "管理员"
                    )
                )
                roleId = await roleProxy.fetchone()
                roleId = roleId[0]
                await conn.execute(sa.insert(self.tables.t_role_mem).values(roleId=roleId, memId=memId))
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def userRole(self, userId, roleId):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(
                    sa.update(self.tables.t_user).values(roleId=roleId).where(self.tables.t_user.c.id == userId)
                )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def roleRights(self, roleId, rightIds):
        """
        不允许更改管理员的权限
        :param roleId:
        :param rightIds:
        :return:
        """
        if not isinstance(rightIds, list):
            raise Exception

        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_role.c.id).where(self.tables.t_role.c.name == "管理员"))
                rootId = await proxy.fetchone()
                rootId = rootId[0]
                if roleId == rootId:
                    raise Exception
                await conn.execute(
                    sa.delete(self.tables.t_role_right).where(self.tables.t_role_right.c.roleId == roleId)
                )
                for rightId in rightIds:
                    await conn.execute(
                        sa.insert(self.tables.t_role_right).values(rightId=rightId, roleId=roleId)
                    )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def roleMems(self, roleId, memIds):
        """
        不允许更改管理员角色的菜单
        修改角色所拥有的菜单
        :param roleId:
        :param memIds:
        :return:
        """
        if not isinstance(memIds, list):
            raise Exception

        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_role.c.id).where(self.tables.t_role.c.name == "管理员"))
                rootId = await proxy.fetchone()
                rootId = rootId[0]
                if roleId == rootId:
                    raise Exception
                await conn.execute(
                    sa.delete(self.tables.t_role_mem).where(self.tables.t_role_mem.c.roleId == roleId)
                )
                for memId in memIds:
                    await conn.execute(
                        sa.insert(self.tables.t_role_mem).values(roleId=roleId, memId=memId)
                    )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def updateUser(self, userId, roleId, username):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(
                    sa.update(self.tables.t_user).values(
                        roleId=roleId, username=username
                    ).where(
                        self.tables.t_user.c.id == userId
                    )
                )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def changePasswd(self, userId, passwd):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(
                    sa.update(self.tables.t_user).values(
                        passwd=passwd
                    ).where(
                        self.tables.t_user.c.id == userId
                    )
                )
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def roleOwnMem(self, roleId):
        data = []
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(
                        self.tables.t_mem.c.id, self.tables.t_mem.c.value
                    ).where(
                        self.tables.t_role_mem.c.memId == self.tables.t_mem.c.id,
                        self.tables.t_role_mem.c.roleId == roleId
                    )
                )
                async for i in proxy:
                    data.append({"id": i[0], "value": i[1]})

            except Exception:
                await trans.rollback()
            else:
                await trans.commit()

        return data
