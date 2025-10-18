import redis
import json
import os
import redis
from dotenv import load_dotenv

load_dotenv()


redis_url = os.getenv('REDIS_URL')
cache = redis.Redis.from_url(redis_url, decode_responses=True)


def get_catched_news(catch_key : str):
    catched_news = cache.get(catch_key)

    if catched_news :
        return catched_news
    return None


def set_cache_news(cache_key:str  ,news_data : dict):
    cache.setex(cache_key , 1800 , json.dumps(news_data))


def delete_cache(cache_key :str):
    cache.delete(cache_key)

