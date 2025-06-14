import streamlit as st
import requests
import redis
from datetime import datetime, timedelta
from finprompt.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
    ssl=True
)

# MAX_REQUESTS_PER_IP = 5
# WINDOW_SECONDS = 3600

MAX_REQUESTS_PER_IP = 25

# def get_user_ip():
#     try:
#         ip = requests.get('https://api.ipify.org', timeout=5).text
#     except Exception:
#         ip = "unknown"
#     return ip

def get_user_ip():
    try:
        ip = requests.get('https://api.ipify.org', timeout=5).text
        if not ip or ip.strip().lower() == "unknown":
            st.warning("Kullanıcı IP adresi alınamadı. Ücretsiz erişim devre dışı bırakıldı, lütfen kendi API anahtarınızı kullanın.")
            return None
        return ip
    except Exception:
        st.warning("Kullanıcı IP adresi alınamadı. Ücretsiz erişim devre dışı bırakıldı, lütfen kendi API anahtarınızı kullanın.")
        return None

def _get_ttl_to_midnight():
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int((tomorrow - now).total_seconds())

def check_and_increment_ip_limit(ip):
    today_str = datetime.now().strftime('%Y-%m-%d')
    key = f"ip_daily_limit:{ip}:{today_str}"
    current = redis_client.get(key)
    ttl = _get_ttl_to_midnight()
    if current is None:
        redis_client.set(key, 1, ex=ttl)
        return True, MAX_REQUESTS_PER_IP - 1
    else:
        current = int(current)
        if current >= MAX_REQUESTS_PER_IP:
            return False, 0
        else:
            redis_client.incr(key)
            redis_client.expire(key, ttl)
            return True, MAX_REQUESTS_PER_IP - current - 1

def get_ip_limit_reset_seconds(ip):
    today_str = datetime.now().strftime('%Y-%m-%d')
    key = f"ip_daily_limit:{ip}:{today_str}"
    ttl = redis_client.ttl(key)
    return ttl if ttl > 0 else 0

# def check_and_increment_ip_limit(ip):
#     key = f"ip_limit:{ip}"
#     current = redis_client.get(key)
#     if current is None:
#         redis_client.set(key, 1, ex=WINDOW_SECONDS)
#         return True, MAX_REQUESTS_PER_IP - 1
#     else:
#         current = int(current)
#         if current >= MAX_REQUESTS_PER_IP:
#             return False, 0
#         else:
#             redis_client.incr(key)
#             redis_client.expire(key, WINDOW_SECONDS)
#             return True, MAX_REQUESTS_PER_IP - current - 1

# def get_ip_limit_reset_seconds(ip):
#     key = f"ip_limit:{ip}"
#     ttl = redis_client.ttl(key)
#     return ttl if ttl > 0 else 0