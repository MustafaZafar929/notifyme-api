import redis
import json


cache = redis.StrictRedis(host='localhost' , port=6379 , db=1)



def get_catched_news(catch_key : str):
    catched_news = cache.get(catch_key)

    if catched_news :
        return catched_news
    return None


def set_cache_news(cache_key:str  ,news_data : dict):
    cache.setex(cache_key , 1800 , json.dumps(news_data))


def delete_cache(cache_key :str):
    cache.delete(cache_key)

