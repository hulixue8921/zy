import asyncio
from lyrra.share.myMysql import MyMysql
import sys
import sqlalchemy as sa

async def run():
    mysql=MyMysql()
    mysqlEn=await mysql.getEn()
    async with mysqlEn.acquire() as conn:
        trans = await conn.begin()
        try:
            await conn.execute(sa.insert(mysql.t_globallock).values(name=sys.argv[1]))
        except Exception as e:
            await trans.rollback()
            return 1
        else:
            await trans.commit()
            return 0 


async def main():
   while True:
       x = await run()
       if x == 0:
          break
       else:
          await asyncio.sleep(5)
       
   sys.exit(0)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
