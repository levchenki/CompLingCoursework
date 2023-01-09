from redis import Redis


class RedisHelper:
    def __init__(self):
        self.client = Redis(
            host='localhost',
            port=6379,
            db=0,
            encoding='utf-8',
            decode_responses=True
        )
