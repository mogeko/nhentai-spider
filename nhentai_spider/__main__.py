from nhentai_spider.backend import FileDownloader
from nhentai_spider.nhentai import IndexPage, MetaPage
from nhentai_spider.spider import Spider
from functools import reduce
from typing import Tuple
import asyncio

async def main():
    async with Spider().creat() as spider:

        async def handle_meta_and_gallery_page(site: MetaPage):
            meta = await spider.fetch(site.get_url())
            gallery = await spider.fetch(f'{site.get_url()}1')
            return site.handle_meta_page(meta.decode()).handle_gallery_page(gallery.decode())

        # Donwload images
        # In order to run CI faster, only save meta.json rather than download images.
        #
        # async def download_imgs(site: MetaPage):
        #     downloader = FileDownloader(site.export())
        #     await downloader.save_meta()
        #     return [
        #         spider.create_task(
        #             downloader.save_imgs(await spider.fetch(url, min_delay=0.1, max_delay=0.5), index)
        #         ) for index, url in enumerate(site.get_downloads(), start=1)
        #     ]

        nhentai = IndexPage()
        index_html = await spider.do(spider.fetch(nhentai.get_url())).join()
        pop_sites: Tuple[MetaPage] = await spider.clean_task().map_jobs(
            handle_meta_and_gallery_page,
            nhentai.handle_index(index_html[0]).pop_page()
        ).join()
        await spider.clean_task().map_jobs(
            lambda site: FileDownloader(site.export()).save_meta(),
            pop_sites
        ).join()

asyncio.run(main())
