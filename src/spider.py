from asyncio.tasks import Task
from contextlib import asynccontextmanager
from random import uniform
from typing import Callable, Iterable
import aiohttp
import asyncio
import logging

loger = logging.getLogger(__name__)

class Spider:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    }

    def __init__(self) -> None:
        '''Create a Spider.'''
        loger.info('the spider is created')
        self.session = aiohttp.ClientSession()
        self.tasks   = []

    @asynccontextmanager
    async def creat(self):
        '''Create a Spider safely.'''
        try:
            yield self
        finally:
            await self.close()

    async def close(self) -> None:
        '''Close underlying connector.

        Release all acquired resources.
        '''
        loger.info('the spider is dead.')
        await self.session.close()

    async def sleep(self, min_delay:float = 1, max_delay: float = 5) -> None:
        '''Coroutine that completes after a random time (in seconds).
        
        Use min_delay and max_delay to specify the range of random time.
        '''
        delay = round(uniform(min_delay, max_delay), 3)
        loger.info('the spider will sleep for %s seconds', delay)
        await asyncio.sleep(delay)

    async def fetch(self, url: str) -> str:
        '''Get HTML from the specified url.'''
        loger.info('get HTML from %s', url)
        await self.sleep() # sleep a random time (between 1s and 5s)
        async with self.session.get(url, headers=self.headers) as response:
            return await response.text()

    async def join(self):
        '''Return the future aggregating results from task list.'''
        loger.debug('the spider started working')
        return await asyncio.gather(*self.tasks)

    def create_task(self, job) -> Task:
        '''Schedule the execution of a coroutine object in a spawn task.

        Return a Task object.
        '''
        loger.debug('creat and return a task')
        return asyncio.create_task(job)

    def extend_task(self, tasks: Iterable):
        '''Extend task list by appending elements from the iterable.'''
        loger.debug('extend the task list')
        self.tasks.extend(tasks)
        return self

    def map_jobs(self, func: Callable, jobs: Iterable):
        '''Make an iterator that computes the function using arguments
        from each of the iterables. Then put the iterables into task list.
        '''
        loger.debug('put some processed jobs into the task list')
        self.extend_task(map(func, jobs))
        return self

    def do(self, job):
        '''Extend list by appending elements from the iterable.'''
        loger.debug('add a job into the task list')
        self.tasks.append(self.create_task(job))
        return self
