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
        'aiohttp>=3.7.4.post0',
        'asyncio>=3.4.3',
        'beautifulsoup4>=4.9.3',
        'fake-useragent>=0.1.11',
        'lxml>=4.6.3'
    ],
    tests_require=[
        'pytest>=6.2.4',
        'pytest-cov>=2.12.1',
        'pytest_asyncio>=0.15.1'
    ],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)
