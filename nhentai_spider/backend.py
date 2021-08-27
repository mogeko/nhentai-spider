from typing import Union
import aiofiles
import logging
import json
import os

loger = logging.getLogger(__name__)

class FileDownloader:

    def __init__(self, meta: dict[str, Union[list[str], str, int]], *, save_path='nhentai') -> None:
        self.save_path = save_path
        self.meta      = meta

    def export_json(self, *, sort_keys=True, indent=4) -> bytes:
        """export meta information in the form of json"""
        loger.debug('export meta infowith json')
        return json.dumps(
            self.meta,
            ensure_ascii=False,
            sort_keys=sort_keys,
            indent=indent
        ).encode('utf-8')

    def mkdir(self) -> str:
        h1title: str = self.meta['h1title']
        workspaces = f'{self.save_path}/{h1title}'
        if not os.path.exists(workspaces):
            loger.info('create folders in %s', workspaces)
            os.makedirs(workspaces)
        return workspaces

    async def save_meta(self):
        """save meta info in the specified folder in json format"""
        file_path = f'{self.mkdir()}/meta.json'
        loger.info('save meta info into %s', file_path)
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as json_file:
            await json_file.write(self.export_json().decode())

    async def save_imgs(self, data: bytes, page: int):
        file_path = f'{self.mkdir()}/{page}.jpg'
        async with aiofiles.open(file_path, 'wb') as img:
            await img.write(data)
