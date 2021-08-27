from typing import Union
import aiofiles
import asyncio
import logging
import json
import os

loger = logging.getLogger(__name__)

class FileDownloader:

    def __init__(self, meta: dict[str, Union[list[str], str, int]]) -> None:
        self.meta = meta

    def export_json(self, *, sort_keys=True, indent=4) -> bytes:
        """export meta information in the form of json"""
        loger.debug('export meta infowith json')
        return json.dumps(
            self.meta,
            ensure_ascii=False,
            sort_keys=sort_keys,
            indent=indent
        ).encode('utf-8')

    async def save_meta(self, *, save_path='nhentai'):
        """save meta info in the specified folder in json format"""
        h1title: str = self.meta['h1title']
        save_path = f'{save_path}/{h1title}'
        file_path = f'{save_path}/meta.json'
        loger.info('save meta info into %s', file_path)
        if not os.path.exists(save_path):
            loger.info('create folders in %s', save_path)
            os.makedirs(save_path)
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as json_file:
            await json_file.write(self.export_json().decode())
