'''
服务模拟
'''
import random
import datetime
from random import randint
import pandas as pd

from engine.engine import engine

random.seed(0)


# 随机生成服务包
def service(num):
    services = []
    for i in range(num):
        service_dict = {}
        service_dict['id'] = i
        service_dict['senior_id'] = randint(1, 30)
        service_dict['time'] = randint(10 * 60, 100 * 60)
        # 最早
        service_dict['earliest'] = randint(0, 12 * 60 * 60)
        # 最迟
        service_dict['latest'] = service_dict['earliest'] + randint(10 * 60, 100 * 60)
        service_dict['loss'] = randint(10, 100000)
        service_dict['worker_type'] = randint(1, 10)
        service_dict['service_type'] = randint(1, 10)
        services.append(service_dict)

    df = pd.DataFrame(services)
    df = df.set_index('id')
    df['create_time'] = datetime.datetime.now()
    return df


if __name__ == '__main__':
    df_services = service(200)
    df_services.to_sql('service', engine, if_exists='replace')
