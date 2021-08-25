from nhentai_spider.nhentai import Template
from example.meta_page import meta
import logging
import pytest

logging.basicConfig(level=logging.DEBUG)

loger = logging.getLogger(__name__)

@pytest.fixture(scope='function', name='setup')
def setup_function(request):
    def teardown_function():
        loger.info('teardown the test')
    request.addfinalizer(teardown_function)
    loger.info('start the test')
    return Template()


def test_handle_meta_page(setup: Template):
    with open('./tests/example/meta_page.html', 'r') as html_file:
        site = setup.handle_meta_page(html_file.read())
        assert setup == site
    assert setup.h1title == meta['h1title']
    assert setup.h2title == meta['h2title']
    assert setup.h1title_full == meta['h1title_full']
    assert setup.h2title_full == meta['h2title_full']
    assert setup.gallery_id == meta['gallery_id']
    assert setup.parodies == meta['parodies']
    assert setup.characters == meta['characters']
    assert setup.tags == meta['tags']
    assert setup.artists == meta['artists']
    assert setup.groups == meta['groups']
    assert setup.languages == meta['languages']
    assert setup.categories == meta['categories']
    assert setup.pages == meta['pages']
    assert setup.up_time == meta['up_time']

if __name__ == '__main__':
    pytest.main()