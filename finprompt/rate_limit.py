import requests
import redis
from finprompt.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
    ssl=True
)

MAX_REQUESTS_PER_IP = 5
WINDOW_SECONDS = 3600

def get_user_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
    except Exception:
        ip = "unknown"
    return ip

def check_and_increment_ip_limit(ip):
    key = f"ip_limit:{ip}"
    current = redis_client.get(key)
    if current is None:
        redis_client.set(key, 1, ex=WINDOW_SECONDS)
        return True, MAX_REQUESTS_PER_IP - 1
    else:
        current = int(current)
        if current >= MAX_REQUESTS_PER_IP:
            return False, 0
        else:
            redis_client.incr(key)
            redis_client.expire(key, WINDOW_SECONDS)
            return True, MAX_REQUESTS_PER_IP - current - 1

def get_ip_limit_reset_seconds(ip):
    key = f"ip_limit:{ip}"
    ttl = redis_client.ttl(key)
    return ttl if ttl > 0 else 0