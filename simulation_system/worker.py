import pandas as pd
import random
import datetime
from random import randint

from engine.engine import engine
random.seed(0)

def worker(num):
    workers = []
    for i in range(num):
        dict = {}
        dict['id'] = i
        dict['type'] = randint(1,10)
        workers.append(dict)
    df = pd.DataFrame(workers)
    df = df.set_index('id')
    df['create_time'] = datetime.datetime.now()

    df.to_sql('worker',engine,if_exists='replace')

if __name__ == '__main__':
    worker(20)