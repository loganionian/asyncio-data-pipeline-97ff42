import asyncio
import logging
from typing import AsyncIterable, Callable, TypeVar, Optional

T = TypeVar('T')
U = TypeVar('U')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Pipe:
    def __init__(self, source: AsyncIterable[T]) -> None:
        self.source = source

    async def __aiter__(self) -> AsyncIterable[T]:
        async for item in self.source:
            yield item

    def map(self, func: Callable[[T], U]) -> 'Pipe':
        logger.debug("Mapping with function: %s", func)
        mapped_source = (func(item) for item in self.source)
        return Pipe(mapped_source)

    def filter(self, func: Callable[[T], bool]) -> 'Pipe':
        logger.debug("Filtering with function: %s", func)
        filtered_source = (item for item in self.source if func(item))
        return Pipe(filtered_source)

async def async_generator() -> AsyncIterable[int]:
    for i in range(20):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for item in Pipe(async_generator()).filter(lambda x: x > 10).map(lambda x: x * 2):
        print(item)

if __name__ == "__main__":
    asyncio.run(main())