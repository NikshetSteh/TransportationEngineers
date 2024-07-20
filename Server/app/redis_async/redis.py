from redis.asyncio import ConnectionPool, Redis


class RedisClient(Redis):
    def __init__(self, connection_pool: ConnectionPool):
        super().__init__(connection_pool=connection_pool)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()


class RedisPool:
    def __init__(self, url: str):
        self.pool = ConnectionPool.from_url(url)

    def __call__(self, *args, **kwargs):
        return RedisClient(self.pool)
