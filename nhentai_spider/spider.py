from asyncio.tasks import Task
from contextlib import asynccontextmanager
from random import uniform
from typing import Awaitable, Callable, Iterable, Tuple, TypeVar, Union
from aiohttp.client_reqrep import ClientRequest
from fake_useragent import UserAgent
import aiohttp
import asyncio
import logging

T = TypeVar('T')
S = TypeVar('S')
U = TypeVar('U')

loger = logging.getLogger(__name__)

class Spider:

    headers = {
        'User-Agent': UserAgent().random
    }

    def __init__(self) -> None:
        """Create a Spider."""
        loger.info('the spider is created')
        self.session = aiohttp.ClientSession()
        self.tasks: list[Task[S]] = []

    @asynccontextmanager
    async def creat(self):
        """Create a Spider safely."""
        try:
            yield self
        finally:
            await self.close()

    async def close(self) -> None:
        """Close underlying connector.

        Release all acquired resources.
        """
        loger.info('the spider is dead.')
        await self.session.close()

    async def sleep(self, min_delay:float = 1, max_delay: float = 5) -> None:
        """Coroutine that completes after a random time (in seconds).

        Use min_delay and max_delay to specify the range of random time.

        set max_delay=0 to close it.
        """
        if max_delay:
            delay = round(uniform(min_delay, max_delay), 3)
            loger.info('the spider will sleep for %s seconds', delay)
            await asyncio.sleep(delay)

    async def fetch(self, url: str, *, min_delay: float = 1, max_delay: float = 5) -> bytes:
        """Get Bytes data from the specified url.

        use min_delay and max_delay to set a random sleep time(default between 1s and 5s).

        set max_delay=0 to pass the sleep time.
        """
        loger.info('get HTML from %s', url)
        await self.sleep(min_delay, max_delay) # sleep a random time (default between 1s and 5s)
        async with self.session.get(url, headers=self.headers) as response:
            if response.status == 200:
                return await response.read()

    async def join(self) -> Tuple[S]:
        """Return the future aggregating results from task list."""
        loger.debug('the spider started working')
        return await asyncio.gather(*self.tasks)

    def create_task(self, job: S) -> Task[S]:
        """Schedule the execution of a coroutine object in a spawn task.

        Return a Task object.
        """
        loger.debug('creat and return a task')
        return asyncio.create_task(job)

    def extend_task(self, tasks: Iterable[Task[S]]):
        """Extend task list by appending elements from the iterable."""
        loger.debug('extend the task list')
        self.tasks.extend(tasks)
        return self

    def clean_task(self):
        """Clean up task list"""
        self.tasks.clear()
        return self

    def map_jobs(self, func: Callable[[T], S], iters: Iterable[T]):
        """Make an iterator that computes the function using arguments
        from each of the iterables. Then put the iterables into task list.
        """
        loger.debug('put some processed jobs into the task list')
        bind = lambda iter: self.create_task(func(iter))
        self.extend_task(map(bind, iters))
        return self

    def do(self, job: Callable[[T], S]):
        """Extend list by appending elements from the iterable."""
        loger.debug('add a job into the task list')
        self.tasks.append(self.create_task(job))
        return self
