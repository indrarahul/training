import redis
import multiprocessing
import argparse
import requests

def consume():
    r = redis.Redis(host='localhost',port=6378)
    d = r.zpopmin('queue')
    requests.post('localhost:8000',data=d)

def parse_args():
    parser = argparse.ArgumentParser(description='consumer - redis',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--numProcess', default=5)
    return parser.parse_args()

def run():
    p = parse_args()
    process = []
    for _ in range(p.numProcess):
        process.append(multiprocessing.Process(target=consume()))

    for p in process:
        p.start()

    for p in process:
        p.join()

    print("All Done")     


if __name__ == '__main__':
    run()