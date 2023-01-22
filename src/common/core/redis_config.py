import os
from dotenv import load_dotenv
import redis

load_dotenv()


MAX_DATA = 100000
HOST = 'localhost'
PORT = 6379


class RedisQueue(object):
    def __init__(self, name, max_size, **redis_kwargs):
        self.key = name
        self.max_size = max_size
        self.rq = redis.Redis(**redis_kwargs)

    def set(self, name, element):
        return self.rq.set(name, element)

    def size(self):  # 큐 크기 확인
        return self.rq.llen(self.key)

    def delete(self):
        return self.rq.flushdb()

    def is_empty(self):  # 비어있는 큐인지 확인
        return self.size() == 0

    def put(self, element):  # 데이터 넣기
        return self.rq.lpush(self.key, element)  # left push

    def put_and_trim(self, element):  # 데이터 넣기
        queue_count = self.rq.lpush(self.key, element)  # left push
        self.rq.ltrim(self.key, 0, self.max_size - 1)  # 최대크기를 초과한 경우 자르기
        return queue_count

    def get(self, is_blocking=False, timeout=None):  # 데이터 꺼내기
        if is_blocking:
            element = self.rq.brpop(self.key, timeout=timeout)  # blocking right pop
            element = element[1]  # key[0], value[1]
        else:
            element = self.rq.rpop(self.key)  # right pop
        return element

    def get_without_pop(self):  # 꺼낼 데이터 조회
        if self.is_empty():
            return None
        element = self.rq.lindex(self.key, -1)
        return element



def redis_config() :
    try:
        q = RedisQueue('raw-data', MAX_DATA, host=HOST, port=PORT, db=0)
    #     REDIS_HOST = str = os.getenv("REDIS_HOST")
    #     REDIS_PORT = integer = os.getenv("REDIS_PORT")
    #     REDIS_DATABASE = integer = os.getenv("REDIS_DATABASE")
        # rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)

    except:
        print("redis connection failure")
    return q
