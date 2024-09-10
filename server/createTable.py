import asyncio
from lyrra.share.myTable import MyTable



async def main():
    tables = MyTable()
    tables.createTable()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
