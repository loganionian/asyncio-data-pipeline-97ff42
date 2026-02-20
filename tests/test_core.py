import pytest
import asyncio
from asyncio_data_pipeline import Pipe

@pytest.mark.asyncio
async def test_pipe():
    async def source():
        yield 1
        yield 2
        yield 3

    async for item in Pipe(source()).map(lambda x: x * 2):
        assert item in {2, 4, 6}

@pytest.mark.asyncio
async def test_filter():
    async def source():
        yield 1
        yield 2
        yield 3

    async for item in Pipe(source()).filter(lambda x: x > 1):
        assert item in {2, 3}

@pytest.mark.asyncio
async def test_combined():
    async def source():
        yield 1
        yield 2
        yield 3

    async for item in Pipe(source()).filter(lambda x: x > 1).map(lambda x: x * 2):
        assert item in {4, 6}

@pytest.mark.asyncio
async def test_empty_source():
    async def empty_source():
        return iter([])

    async for item in Pipe(empty_source()).map(lambda x: x * 2):
        assert False, "Should not yield any items"

@pytest.mark.asyncio
async def test_error_handling():
    async def source():
        yield 1
        yield 2
        yield 3

    with pytest.raises(Exception):
        async for item in Pipe(source()).map(lambda x: 1 / 0):
            pass