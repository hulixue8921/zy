import configparser
import aiomysql
from aiomysql.sa import create_engine
from lyrra.share.myTable import MyTable
import sqlalchemy as sa

globalDict = {}


def wapper(cls):
    def A(*args, **kwargs):
        if cls not in globalDict:
            globalDict[cls] = cls(*args, **kwargs)
        return globalDict[cls]

    return A


@wapper
class MyMysql(MyTable):
    def __init__(self):
        super().__init__()
        self.engine = None

    async def getEn(self):
        if self.engine is None:
            self.engine = await create_engine(
                user=self.user,
                db=self.db,
                host=self.ip,
                password=self.passwd,
                minsize=self.min,
                maxsize=self.max,
                pool_recycle=3600
            )
        return self.engine

    async def initData(self):
        self.createTable()
        async with self.engine.acquire() as conn:
            trans = await conn.begin()
            try:
                await conn.execute(sa.insert(self.t_role).values(name="匿名角色"))
                await conn.execute(sa.insert(self.t_role).values(name="管理员"))
                roleId = await conn.execute("SELECT LAST_INSERT_ID()")
                rId = await roleId.fetchone()
                rId = rId[0]
                await conn.execute(sa.insert(self.t_user).values(username="root", passwd="123456", roleId=rId))

                await conn.execute(sa.insert(self.t_mem).values(value="系统管理:用户管理"))
                memId = await conn.execute("SELECT LAST_INSERT_ID()")
                mId = await memId.fetchone()
                mId = mId[0]
                await conn.execute(sa.insert(self.t_role_mem).values(roleId=rId, memId=mId))

                await conn.execute(sa.insert(self.t_mem).values(value="系统管理:角色管理"))
                memId = await conn.execute("SELECT LAST_INSERT_ID()")
                mId = await memId.fetchone()
                mId = mId[0]
                await conn.execute(sa.insert(self.t_role_mem).values(roleId=rId, memId=mId))

                await conn.execute(sa.insert(self.t_mem).values(value="app管理:app列表"))
                memId = await conn.execute("SELECT LAST_INSERT_ID()")
                mId = await memId.fetchone()
                mId = mId[0]
                await conn.execute(sa.insert(self.t_role_mem).values(roleId=rId, memId=mId))

                await conn.execute(sa.insert(self.t_mem).values(value="app管理:app操作"))
                memId = await conn.execute("SELECT LAST_INSERT_ID()")
                mId = await memId.fetchone()
                mId = mId[0]
                await conn.execute(sa.insert(self.t_role_mem).values(roleId=rId, memId=mId))

                await conn.execute(sa.insert(self.t_right).values(value="admin", name="管理员超级权限"))
                memId = await conn.execute("SELECT LAST_INSERT_ID()")
                mId = await memId.fetchone()
                mId = mId[0]
                await conn.execute(sa.insert(self.t_role_right).values(roleId=rId, rightId=mId))

                await conn.execute(sa.insert(self.t_right).values(value="app::cms", name="app管理权限"))
                memId = await conn.execute("SELECT LAST_INSERT_ID()")
                mId = await memId.fetchone()
                mId = mId[0]
                await conn.execute(sa.insert(self.t_role_right).values(roleId=rId, rightId=mId))

                await conn.execute(sa.insert(self.t_env).values(name="dev"))
                await conn.execute(sa.insert(self.t_env).values(name="test"))
                await conn.execute(sa.insert(self.t_env).values(name="pre"))
                await conn.execute(sa.insert(self.t_env).values(name="prod"))


            except Exception:
                await trans.rollback()
            else:
                await trans.commit()
