from typing import Tuple
from nhentai_spider.nhentai import IndexPage, MetaPage
from nhentai_spider.spider import Spider
import asyncio

async def main():
    async with Spider().creat() as spider:

        async def handle_meta_page(site: MetaPage):
            html = await spider.fetch(site.get_url())
            return site.handle_meta_page(html)   

        async def handle_gallery_page(site: MetaPage) -> Tuple[MetaPage]:

            async def handle_gallery_page_iter(page: int):
                html = await spider.fetch(f'{site.get_url()}/{page}')
                return site.handle_gallery_page(html)

            return await spider.clean_task().map_jobs(
                handle_gallery_page_iter, range(1, site.pages)
            ).join()

        nhentai = IndexPage()
        index_html = await spider.do(spider.fetch(nhentai.index)).join()
        pop_sites: Tuple[MetaPage] = await spider.clean_task().map_jobs(
            handle_meta_page,
            nhentai.handle_index(index_html[0]).pop_page()
        ).join()

asyncio.run(main())
