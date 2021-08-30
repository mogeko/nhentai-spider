from bs4 import BeautifulSoup
from nhentai_spider.nhentai import MetaPage, IndexPage, IndexPageLanguage, IndexPagePopAndNew
from example.index_page import index
from example.meta_page import meta
import logging
import pytest

logging.basicConfig(level=logging.DEBUG)

loger = logging.getLogger(__name__)

#
# Test IndexPage
#
@pytest.fixture(name='index_page')
def setup_index_page():
    loger.info('start the IndexPage')
    yield IndexPage()
    loger.info('teardown the IndexPage')

def test_get_url_in_IndexPage(index_page: IndexPage):
    assert index_page.get_url()  == index['index']

def test_set_language(index_page: IndexPage):
    assert type(index_page.set_language('chinese')) == IndexPageLanguage

def test_get_gallery_url(index_page: IndexPage):
    with open('./tests/example/index_gallery_url.html', 'r') as html_file:
        soup = BeautifulSoup(html_file.read(), 'lxml')
    assert index_page.get_gallery_url(soup) == ['https://nhentai.nethttps://nhentai.net/g/371243/']

def test_handle_index_in_IndexPage(index_page: IndexPage):
    with open('./tests/example/index_page.html', 'r') as html_file:
        site = index_page.handle_index(html_file.read())
    assert type(site) == IndexPagePopAndNew

#
# Test _IndexPage__PopAndNew
#
@pytest.fixture(name='pop_and_new')
def setup_index_page_with_pop_and_new():
    loger.info('atart the IndexPage with pop&new page')
    yield IndexPagePopAndNew(index['popular'], index['new'])
    loger.info('teardown the IndexPage with pop&new page')

def test_pop_site(pop_and_new: IndexPagePopAndNew):
    sites = pop_and_new.pop_page()
    for site, url in zip(sites, index['popular']):
        assert type(site) == MetaPage
        assert site.get_url() == url

def test_new_site(pop_and_new: IndexPagePopAndNew):
    sites = pop_and_new.new_page()
    for site, url in zip(sites, index['new']):
        assert type(site) == MetaPage
        assert site.get_url() == url

#
# Test MetaPage
#
@pytest.fixture(name='meta_page')
def setup_meta_page():
    loger.info('start the MetaPage')
    yield MetaPage('only for test', pages=33)
    loger.info('teardown the MetaPage')

def test_handle_meta_page(meta_page: MetaPage):
    with open('./tests/example/meta_page.html', 'r') as html_file:
        site = meta_page.handle_meta_page(html_file.read())
    assert type(site)             == MetaPage
    assert meta_page.h1title      == meta['h1title']
    assert meta_page.h2title      == meta['h2title']
    assert meta_page.h1title_full == meta['h1title_full']
    assert meta_page.h2title_full == meta['h2title_full']
    assert meta_page.gallery_id   == meta['gallery_id']
    assert meta_page.parodies     == meta['parodies']
    assert meta_page.characters   == meta['characters']
    assert meta_page.tags         == meta['tags']
    assert meta_page.artists      == meta['artists']
    assert meta_page.groups       == meta['groups']
    assert meta_page.languages    == meta['languages']
    assert meta_page.categories   == meta['categories']
    assert meta_page.pages        == meta['pages']
    assert meta_page.up_time      == meta['up_time']

def test_handle_gallery_page(meta_page: MetaPage):
    with open('./tests/example/gallery_page.html', 'r') as html_file:
        site = meta_page.handle_gallery_page(html_file.read())
    assert type(site)          == MetaPage
    assert meta_page.downloads == meta['downloads']

def test_get_url(meta_page: MetaPage):
    assert meta_page.get_url() == 'only for test'


#
# Test _IndexPage__Language
#
@pytest.fixture(name='language')
def setup_index_page_with_language():
    loger.info('start the MetaPage')
    yield IndexPageLanguage('nhentai.net', 'chinese')
    loger.info('teardown the MetaPage')

def test_get_url_in_IndexPageLanguage(language: IndexPageLanguage):
    language.get_url()        == 'https://nhentai.net/language/chinese/'
    language.get_url(sort='today') == 'https://nhentai.net/language/chinese/popular-today'
    language.get_url(sort='week')  == 'https://nhentai.net/language/chinese/popular-week'
    language.get_url(sort='all')   == 'https://nhentai.net/language/chinese/popular'

def test_handle_index_in_IndexPageLanguage(language: IndexPageLanguage):
    with open('./tests/example/index_lang.html', 'r') as html_file:
        sites = language.handle_index(html_file.read())
        for site in sites:
            assert type(site) == MetaPage


if __name__ == '__main__':
    pytest.main()
