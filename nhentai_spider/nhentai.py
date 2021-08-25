from bs4 import BeautifulSoup

class Template:

    def __init__(self, domain='nhentai.net') -> None:
        self.index  = f'https://{domain}'
        self.domain = domain

    def handle_index(self):
        pass

    def handle_meta_page(self, html: str):
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

        return self

    def handle_gallery_page(self):
        pass
