
import asyncio


async def do_something():
    return 'foo'


async def build_string():
    prefix = await do_something()
    if prefix != 'foo':
        raise ValueError
    return prefix + ' bar'


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(build_string())
    print(result)
