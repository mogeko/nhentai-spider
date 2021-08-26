from typing import Callable, Iterable
from bs4 import BeautifulSoup
import logging

loger = logging.getLogger(__name__)

class MetaPage:

    def __init__(self, url: str) -> None:
        self.url = url

    def get_url(self):
        return self.url

    def handle_meta_page(self, html: str):
        """handle meta page."""
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

    def handle_gallery_page(self):
        pass

class IndexPage:

    def __init__(self, domain='nhentai.net') -> None:
        self.index  = f'https://{domain}'
        self.domain = domain

    def handle_index(self, html: str):

        def get_gallery_url(soup: BeautifulSoup) -> str:
            galleries = soup.find_all(class_='gallery')
            return [self.index + gallery.find('a').get('href') for gallery in galleries]

        loger.info('start handle the index page')
        soup = BeautifulSoup(html, 'lxml').find_all(class_='index-container')

        self.popular = get_gallery_url(soup[0])
        self.new     = get_gallery_url(soup[1])

        loger.debug('[index] popular: %s', self.popular)
        loger.debug('[index] new: %s', self.new)

        return self
    
    def pop_page(self) -> Iterable[MetaPage]:
        return map(MetaPage, self.popular)

    def new_page(self) -> Iterable[MetaPage]:
        return map(MetaPage, self.new)
