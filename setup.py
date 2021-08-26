from setuptools import setup, find_packages

setup(
    name="nhentai_spider",
    version="0.0.1",
    author="mogeko",
    author_email="zhengjunyi@live.com",
    description="A Python spider that crawls nHentai.",
    url="https://github.com/Mogeko/nhentai-spider",
    packages=find_packages(),

    install_requires=[
        'aiohttp',
        'asyncio',
        'BeautifulSoup4',
        'fake-useragent',
        'lxml'
    ],
    tests_require=[
        'pytest>=6.2.4',
        'pytest-cov>=2.12.1',
    ],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)
