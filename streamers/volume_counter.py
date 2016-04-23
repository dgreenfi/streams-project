import redis
from collections import Counter
import urllib2
import time
REDIS_PORT=9999
conn_top=redis.Redis(port=REDIS_PORT,db=4)
conn_top_title=redis.Redis(port=REDIS_PORT,db=5)
conn_hashtag=redis.Redis(db=2,port=REDIS_PORT)
conn_hashtag_counts=redis.Redis(db=6,port=REDIS_PORT)