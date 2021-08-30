from typing import Iterable, Union
from bs4 import BeautifulSoup
import logging

loger = logging.getLogger(__name__)

class IndexPage:

    def __init__(self, domain='nhentai.net') -> None:
        self.__domain = domain

    def set_language(self, lang: str):
        return _IndexPage__Language(self.__domain, lang)

    def get_url(self):
        return f'https://{self.__domain}'

    def __get_gallery_url(self, soup: BeautifulSoup) -> str:
        galleries = soup.find_all(class_='gallery')
        return [self.get_url() + gallery.find('a').get('href') for gallery in galleries]

    def handle_index(self, html: str):

        loger.info('start handle the index page.')
        soup = BeautifulSoup(html, 'lxml').find_all(class_='index-container')

        popular = self.__get_gallery_url(soup[0])
        new     = self.__get_gallery_url(soup[1])

        loger.debug('[index] popular: %s', popular)
        loger.debug('[index] new: %s', new)

        return _IndexPage__PopAndNew(popular, new)


class MetaPage:

    def __init__(self, url: str, *, pages: int = 1) -> None:
        self.pages = pages # for test, default 1
        self.url = url

    def get_url(self):
        """get the url of the work site"""
        return self.url

    def handle_meta_page(self, html: str):
        """handle meta page"""
        loger.info('handle meta from %s', self.url)
        soup = BeautifulSoup(html, 'lxml')
        h1   = soup.find('h1', class_='title')
        h2   = soup.find('h2', class_='title')
        meta = soup.find(id='tags').find_all(class_='tag-container')

        self.h1title      = h1.find(class_='pretty').string
        self.h1title_full = h1.text
        self.h2title      = h2.find(class_='pretty').string
        self.h2title_full = h2.text
        self.gallery_id   = soup.find(id='gallery_id').text
        self.parodies     = [tag.string for tag in meta[0].find_all(class_='name')]
        self.characters   = [tag.string for tag in meta[1].find_all(class_='name')]
        self.tags         = [tag.string for tag in meta[2].find_all(class_='name')]
        self.artists      = [tag.string for tag in meta[3].find_all(class_='name')]
        self.groups       = [tag.string for tag in meta[4].find_all(class_='name')]
        self.languages    = [tag.string for tag in meta[5].find_all(class_='name')]
        self.categories   = [tag.string for tag in meta[6].find_all(class_='name')]
        self.pages        = int(meta[7].find(class_='name').string)
        self.up_time      = meta[8].find('time')['datetime']

        loger.debug('[meta] h1title: %s', self.h1title)
        loger.debug('[meta] h1title_full: %s', self.h1title_full)
        loger.debug('[meta] h2title: %s', self.h2title)
        loger.debug('[meta] h2title_full: %s', self.h2title_full)
        loger.debug('[meta] gallery_id: %s', self.gallery_id)
        loger.debug('[meta] parodies: %s', self.parodies)
        loger.debug('[meta] characters: %s', self.characters)
        loger.debug('[meta] tags: %s', self.tags)
        loger.debug('[meta] artists: %s', self.artists)
        loger.debug('[meta] groups: %s', self.groups)
        loger.debug('[meta] languages: %s', self.languages)
        loger.debug('[meta] categories: %s', self.categories)
        loger.debug('[meta] pages: %s', self.pages)
        loger.debug('[meta] up_time: %s', self.up_time)

        return self

    def handle_gallery_page(self, html: str):
        """handle gallery page, get download urls"""
        loger.info('start handle gallery page.')
        url_head = 'https://i.nhentai.net/galleries'
        soup = BeautifulSoup(html, 'lxml').find(id='image-container')
        img_id  = soup.find('img').get('src').split('/')[4]
        self.downloads = [f'{url_head}/{img_id}/{page}.jpg' for page in range(1, self.pages)]

        for url in self.downloads:
            loger.debug('[dl] get download url: %s', url)

        return self

    def get_downloads(self) -> list[str]:
        return self.downloads

    def export(self) -> dict[str, Union[list[str], str, int]]:
        return {
            'h1title': self.h1title,
            'h2title': self.h2title,
            'h1title_full': self.h1title_full,
            'h2title_full': self.h2title_full,
            'gallery_id': self.gallery_id,
            'parodies': self.parodies,
            'characters': self.characters,
            'tags': self.tags,
            'artists': self.artists,
            'groups': self.groups,
            'languages': self.languages,
            'categories': self.categories,
            'pages': self.pages,
            'up_time': self.up_time,
            'downloads': self.downloads
        }


class _IndexPage__PopAndNew(IndexPage):

    def __init__(self, popular: str, new: str):
        self.__popular = popular
        self.__new     = new

    def pop_page(self) -> Iterable[MetaPage]:
        """return a iterable that encapsulates popular MetaPage"""
        loger.info('get comics that popular now.')
        return map(MetaPage, self.__popular)

    def new_page(self) -> Iterable[MetaPage]:
        """return a iterable that encapsulates new MetaPage"""
        loger.info('get comics that new.')
        return map(MetaPage, self.__new)


class _IndexPage__Language(IndexPage):

    def __init__(self, domain: str, lang: str) -> None:
        self.__domain = domain
        self.__lang   = lang

    def get_url(self, *, sort: str = 'recent'):
        if sort == 'today':
            sort = 'popular-today'
        elif sort == 'week':
            sort = 'popular-week'
        elif sort == 'all':
            sort = 'popular'
        else:
            sort = ''
        return f'https://{self.__domain}/language/{self.__lang}/{sort}'
