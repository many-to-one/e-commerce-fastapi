import json
import asyncio_redis
from datetime import datetime

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
    

    def json_serializer(self, obj):
        """JSON serializer for objects not serializable by default, such as datetime."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


    async def set_value(self, key: str, value: any):
        """Set a key-value pair."""
        connection = await self.connect()
        
        # Serialize Python objects (like lists, dicts, and dates) to JSON strings
        if not isinstance(value, str):
            value = json.dumps(value, default=self.json_serializer)
        
        await connection.set(key, value)

    
    async def get_value(self, key: str):
        """Get the value of a key."""
        connection = await self.connect()
        value = await connection.get(key)
        if value:
            # Deserialize JSON strings back into Python objects
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value  # Return as-is if it's not JSON-encoded
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
