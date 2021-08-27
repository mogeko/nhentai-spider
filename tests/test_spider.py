from os import WIFSTOPPED
from nhentai_spider.spider import Spider
import logging
import pytest
import re

logging.basicConfig(level=logging.DEBUG)

loger = logging.getLogger(__name__)

@pytest.mark.asyncio
@pytest.fixture(name='spider')
async def setup_spider():
    async with Spider().creat() as spider:
        loger.info('start the Spider')
        yield spider
    loger.info('teardown the Spider')

@pytest.mark.asyncio
async def test_fetch(spider: Spider):
    url  = 'https://nhentai.net'
    html = await spider.fetch(url, max_delay=0)
    assert re.findall(r'nhentai.net', html)

@pytest.mark.asyncio
async def test_sleep_default(spider: Spider):
    await spider.sleep()

@pytest.mark.asyncio
async def test_pass_sleep(spider: Spider):
    await spider.sleep(max_delay=0)

@pytest.mark.asyncio
async def test_create_task(spider: Spider):
    await spider.create_task(spider.sleep(max_delay=0))
    for task in spider.tasks:
        assert task

@pytest.mark.asyncio
async def test_do_join(spider: Spider):
    await spider.do(spider.sleep(max_delay=0)).join()

if __name__ == '__main__':
    pytest.main()
