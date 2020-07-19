import random
import redis
import uuid

def main():
    r = redis.Redis(host='localhost', port=6378)
    while True:
        r.zincrby('queue', 1, str(uuid.uuid1()))

if __name__ == '__main__':
    main()