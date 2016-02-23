import redis
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, socket_connect_timeout=0)
r.ping()
