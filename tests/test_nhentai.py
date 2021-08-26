from nhentai_spider.nhentai import MetaPage, IndexPage
from example.index_page import index
from example.meta_page import meta
import logging
import pytest

logging.basicConfig(level=logging.DEBUG)

loger = logging.getLogger(__name__)

@pytest.fixture(scope='function', name='index_page')
def setup_index_page(request):
    def teardown_index_page():
        loger.info('teardown the IndexPage')
    request.addfinalizer(teardown_index_page)
    loger.info('start the IndexPage')
    return IndexPage()

@pytest.fixture(scope='function', name='meta_page')
def setup_meta_page(request):
    def teardown_meta_page():
        loger.info('teardown the MetaPage')
    request.addfinalizer(teardown_meta_page)
    loger.info('start the MetaPage')
    return MetaPage("")

def test_index_page_default(index_page: IndexPage):
    assert index_page.domain == index['domain']
    assert index_page.index  == index['index']

def test_handle_index(index_page: IndexPage):
    with open('./tests/example/index_page.html', 'r') as html_file:
        site = index_page.handle_index(html_file.read())
        assert index_page == site
    assert index_page.popular == index['popular']
    assert index_page.new     == index['new']

def test_handle_meta_page(meta_page: MetaPage):
    with open('./tests/example/meta_page.html', 'r') as html_file:
        site = meta_page.handle_meta_page(html_file.read())
        assert meta_page == site
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

if __name__ == '__main__':
    pytest.main()