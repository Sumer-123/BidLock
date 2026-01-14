import redis

def get_redis_client():
    # Connect to the Redis container running on localhost
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)