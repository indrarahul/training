from redis import Redis
from rq import Queue
from mars_data import fetch_pics

q = Queue(connection=Redis(host='localhost',port=6379))

for i in range(20):
    q.enqueue(fetch_pics,100+i)