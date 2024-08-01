import asyncio
import select
import sys


async def async_input(
        title: str = "> ",
        sep: str = " "
):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, title)
