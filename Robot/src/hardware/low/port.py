import asyncio
import serial_asyncio


class Port:
    def __init__(self, port, baud_rate: int, loop=None):
        self.port = port
        self.baud_rate = baud_rate
        self.reader = None
        self.writer = None
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

    async def open(self):
        self.reader, self.writer = await serial_asyncio.open_serial_connection(
            url=self.port, loop=self.loop, baudrate=self.baud_rate
        )

    async def close(self):
        pass

    async def __aenter__(self) -> "Port":
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def read(self):
        sep = "\n"
        data = await self.reader.readuntil(sep.encode())
        return data

    async def write(self, data):
        await self.writer.write(data)
