import click
import asyncio
from .core import Pipe, async_generator

@click.command()
@click.option('--filter', default=None, help='Filter function as a string (e.g. "lambda x: x > 10")')
@click.option('--map', default=None, help='Map function as a string (e.g. "lambda x: x * 2")')
def cli(filter, map):
    """CLI for asyncio-data-pipeline."""
    filter_func = eval(filter) if filter else lambda x: True
    map_func = eval(map) if map else lambda x: x

    async def run_pipeline():
        async for item in Pipe(async_generator()).filter(filter_func).map(map_func):
            click.echo(item)

    asyncio.run(run_pipeline())

if __name__ == '__main__':
    cli()