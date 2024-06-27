import asyncio

from lyrra import Lyrra
from lyrra.share.myMysql import MyMysql
from lyrra.share.myTable import MyTable
import configparser
import time
import sqlalchemy as sa
from sqlalchemy import or_
import subprocess
import os


class App:
    def __init__(self):
        self.mysql = MyMysql()
        self.tables = MyTable()

    async def addApp(self, name, project, git):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(sa.insert(self.tables.t_app).values(name=name, project=project, git=git))
                appId = await conn.execute("SELECT LAST_INSERT_ID()")
                aId = await appId.fetchone()
                aId = aId[0]
                proxy = await conn.execute(sa.select(self.tables.t_env.c.id))
                async for i in proxy:
                    await conn.execute(sa.insert(self.tables.t_fabu).values(appId=aId, envId=i[0]))
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def delApp(self, appId):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_fabu.c.id).where(self.tables.t_fabu.c.appId == appId))
                async for i in proxy:
                    await conn.execute(
                        sa.delete(self.tables.t_role_fabu).where(self.tables.t_role_fabu.c.fabuId == i[0]))
                await conn.execute(sa.delete(self.tables.t_fabu).where(self.tables.t_fabu.c.appId == appId))
                await conn.execute(sa.delete(self.tables.t_app).where(self.tables.t_app.c.id == appId))
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def listFabu(self, roleId):
        data = []
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(
                        self.tables.t_fabu.c.id,
                        self.tables.t_env.c.name,
                        self.tables.t_app.c.project,
                        self.tables.t_app.c.name,
                        self.tables.t_app.c.git,
                        self.tables.t_fabu.c.commit
                    ).where(
                        self.tables.t_role_fabu.c.roleId == roleId,
                        self.tables.t_app.c.id == self.tables.t_fabu.c.appId,
                        self.tables.t_fabu.c.envId == self.tables.t_env.c.id,
                        self.tables.t_role_fabu.c.fabuId == self.tables.t_fabu.c.id
                    )
                )
                async for i in proxy:
                    data.append({'fabuId': i[0], 'envName': i[1], 'projectName': i[2], 'appName': i[3], 'git': i[4],
                                 'commit': i[5]})
            except Exception:
                await trans.rollback()
            else:
                await trans.commit()

        return data

    async def listApp(self):
        data = []
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_app.c.id, self.tables.t_app.c.name, self.tables.t_app.c.project))
                async for i in proxy:
                    data.append({'appId': i[0], 'appName': i[1], 'projectName': i[2]})
            except Exception:
                await trans.rollback()
            else:
                await trans.commit()
        return data

    async def appAction(self, envName, appName, actionType):
        def fun():
            script = "scripts" + "/" + appName + "-" + envName + "-" + actionType + ".sh"
            if os.path.exists(script):
                res = subprocess.run(['bash', script], stdout=subprocess.PIPE, encoding='utf8')
                code = res.returncode
                return res.stdout
            else:
                return script + "执行脚本不存在"

        loop = asyncio.get_event_loop()
        fetu = loop.run_in_executor(None, fun)
        result = await fetu
        return result

    async def fabu(self, envName, appName, gitAddress, gitCommit):
        def fun():
            data = {}
            script = "scripts" + "/" + appName + "-" + envName + "-" + "fabu" + ".sh"
            if os.path.exists(script):
                res = subprocess.run(['bash', script, gitAddress, gitCommit], stdout=subprocess.PIPE, encoding='utf8')
                data['code'] = res.returncode
                data['message'] = res.stdout
            else:
                data['code'] = 1
                data['message'] = script + "执行脚本不存在"
            return data

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, fun)
        if result['code'] == 0:
            mysqlEn = await self.mysql.getEn()
            async with mysqlEn.acquire() as conn:
                trans = await conn.begin()
                try:
                    proxy = await conn.execute(
                        sa.select(self.tables.t_env.c.id).where(self.tables.t_env.c.name == envName))
                    envId = await proxy.fetchone()
                    eId = envId[0]
                    proxy = await conn.execute(
                        sa.select(self.tables.t_app.c.id).where(self.tables.t_app.c.name == appName))
                    appId = await proxy.fetchone()
                    aId = appId[0]
                    await conn.execute(
                        sa.update(self.tables.t_fabu).values(commit=gitCommit).where(self.tables.t_fabu.c.appId == aId,
                                                                                     self.tables.t_fabu.c.envId == eId))
                except Exception:
                    await trans.rollback()
                else:
                    await trans.commit()
        return result['message']

    async def roleFabu(self, roleId, fabuIds):
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(sa.delete(self.tables.t_role_fabu).where(self.tables.t_role_fabu.c.roleId == roleId))
                for i in fabuIds:
                    await conn.execute(sa.insert(self.tables.t_role_fabu).values(roleId=roleId, fabuId=i))
            except Exception:
                await trans.rollback()
                return False
            else:
                await trans.commit()
                return True

    async def listAppFabu(self, appId):
        data = []
        mysqlEn = await self.mysql.getEn()
        async with mysqlEn.acquire() as conn:
            trans = await conn.begin()
            try:
                proxy = await conn.execute(
                    sa.select(self.tables.t_app.c.name, self.tables.t_env.c.name, self.tables.t_fabu.c.id).where(
                        self.tables.t_app.c.id == self.tables.t_fabu.c.appId,
                        self.tables.t_env.c.id == self.tables.t_fabu.c.envId,
                        self.tables.t_app.c.id == appId
                    )
                )
                async for i in proxy:
                    data.append({"appName": i[0], "envName": i[1], "fabuId": i[2]})
            except Exception:
                await  trans.rollback()
            else:
                await  trans.commit()

        return data
