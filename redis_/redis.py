import asyncio_redis

class RedisClient:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self):
        """Establish Redis connection."""
        if self.connection is None:
            self.connection = await asyncio_redis.Connection.create(host=self.host, port=self.port)
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

    async def update_value(self, key: str, new_value: str):
        """Update the value of a key."""
        connection = await self.connect()
        existing_value = await connection.get(key)
        if existing_value is None:
            return None
        await connection.set(key, new_value)
        return new_value

    async def delete_value(self, key: str):
        """Delete a key-value pair."""
        connection = await self.connect()
        existing_value = await connection.get(key)
        if existing_value is None:
            return None
        await connection.delete([key])
        return key

    async def close(self):
        """Close the Redis connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
