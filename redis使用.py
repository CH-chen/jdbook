import redis


conn = redis.Redis(host="192.168.170.141",port=6379,password="chenchen")
keys = conn.keys()
print(keys)