import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisCache:
    def __init__(self):
        self.client = redis.from_url(REDIS_URL, decode_responses=True)

    def set_state(self, key: str, value: str, ex: int = 3600):
        self.client.set(key, value, ex=ex)

    def get_state(self, key: str):
        return self.client.get(key)

    def publish_update(self, channel: str, message: str):
        self.client.publish(channel, message)

redis_cache = RedisCache()
