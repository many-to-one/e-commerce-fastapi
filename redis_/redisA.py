# import redis.asyncio as aioredis
from redis.asyncio import Redis

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self):
        """Establish Redis connection."""
        if self.connection is None:
            self.connection = Redis(host=self.host, port=self.port)
        return self.connection

    async def set_value(self, key: str, value: str):
        """Set a key-value pair."""
        connection = await self.connect()
        await connection.set(key, value)

    async def get_value(self, key: str):
        """Get the value of a key."""
        connection = await self.connect()
        value = await connection.get(key)
        return value

    async def close(self):
        """Close the Redis connection."""
        if self.connection:
            await self.connection.close()
            self.connection = None
