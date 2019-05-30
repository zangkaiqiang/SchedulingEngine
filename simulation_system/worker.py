import pandas as pd
import random
import datetime
from random import randint

from engine.engine import engine

random.seed(0)


def worker(num):
    workers = []
    for i in range(num):
        worker_dict = {}
        worker_dict['id'] = i
        worker_dict['type'] = randint(1, 10)
        workers.append(worker_dict)
    df = pd.DataFrame(workers)
    df = df.set_index('id')
    df['create_time'] = datetime.datetime.now()

    return df


if __name__ == '__main__':
    df_worker = worker(20)
    df_worker.to_sql('worker', engine, if_exists='replace')
