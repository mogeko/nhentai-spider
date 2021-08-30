from nhentai_spider.nhentai import MetaPage, IndexPage, _IndexPage__PopAndNew
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

def test_get_url_in_index_page(index_page: IndexPage):
    assert index_page.get_url()  == index['index']

def test_handle_index(index_page: IndexPage):
    with open('./tests/example/index_page.html', 'r') as html_file:
        site = index_page.handle_index(html_file.read())
    assert type(site) == _IndexPage__PopAndNew

#
# Test _IndexPage__PopAndNew
#
@pytest.fixture(name='pop_and_new')
def setup_index_with_pop_and_new_page():
    loger.info('atart the IndexPage with pop&new page')
    yield _IndexPage__PopAndNew(index['popular'], index['new'])
    loger.info('teardown the IndexPage with pop&new page')

def test_pop_site(index_page: _IndexPage__PopAndNew):
    with open('./tests/example/index_page.html', 'r') as html_file:
        site1 = index_page.handle_index(html_file.read()).pop_page()
        site2 = map(MetaPage, index['popular'])
    for site in zip(site1, site2):
        assert type(site[0]) == MetaPage
        assert type(site[1]) == MetaPage
        assert site[0].url   == site[1].url

def test_new_site(index_page: _IndexPage__PopAndNew):
    with open('./tests/example/index_page.html', 'r') as html_file:
        site1 = index_page.handle_index(html_file.read()).new_page()
        site2 = map(MetaPage, index['new'])
    for site in zip(site1, site2):
        assert type(site[0]) == MetaPage
        assert type(site[1]) == MetaPage
        assert site[0].url   == site[1].url

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


if __name__ == '__main__':
    pytest.main()
