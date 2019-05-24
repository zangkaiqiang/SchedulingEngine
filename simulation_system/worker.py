from random import randint
import random
random.seed(0)

def worker(num):
    workers = []
    for i in range(num):
        dict = {}
        dict['id'] = i
        dict['type'] = randint(1,num)
        workers.append(dict)
    return workers

if __name__ == '__main__':
    worker(10)