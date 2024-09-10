import asyncio
from lyrra.share.myMysql import MyMysql
import sys
import sqlalchemy as sa

async def main():
    mysql=MyMysql()
    mysqlEn=await mysql.getEn()
    async with mysqlEn.acquire() as conn:
        trans = await conn.begin()
        try:
            await conn.execute(sa.delete(mysql.t_globallock).where(mysql.t_globallock.c.name==sys.argv[1]))
        except Exception as e:
            await trans.rollback()
            print(e)
            sys.exit(1)
        else:
            await trans.commit() 

    sys.exit(0)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
