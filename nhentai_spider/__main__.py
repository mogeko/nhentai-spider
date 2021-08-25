from nhentai_spider.spider import Spider
import asyncio

async def main():
    async with Spider().creat() as spider:
        await spider.do(
            spider.fetch('https://www.baidu.com')
        ).do(
            spider.fetch('https://www.google.com')
        ).join()

asyncio.run(main())
