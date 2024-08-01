import asyncio


async def async_input(
        title: str = "> "
):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, title)
