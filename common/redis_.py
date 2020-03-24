import redis

from policy_crawl.config import redis_port,redis_ip

r=redis.Redis(redis_ip,redis_port,decode_responses=True)


