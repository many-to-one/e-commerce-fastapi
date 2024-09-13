from http.client import HTTPException
from redis_.redis import RedisClient


client = RedisClient()


class RedisService:
    def __init__(self):
        self.client = RedisClient()
        
    async def set_value(self, key: str, value: str):
        try:
            await self.client.set_value(key, value)
            return {"message": f"Key '{key}' set with value '{value}'."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    async def get_value(self, key: str):
        try:
            value = await self.client.get_value(key)
            return value
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))