'''
服务模拟
'''
import pandas as pd
import random
import datetime
from random import randint

from engine.engine import engine


random.seed(0)


#随机生成服务包
def service(num):
    services = []
    for i in range(num):
        dict = {}
        dict['id'] = i
        dict['senior_id'] = randint(1,30)
        dict['time'] = randint(10*60,100*60)
        dict['start'] = randint(0,12*60*60)
        dict['end'] = dict['start']+randint(10*60,100*60)
        dict['loss'] = randint(10,100000)
        dict['worker_type'] = randint(1,10)
        dict['service_type'] = randint(1,10)
        services.append(dict)

    df = pd.DataFrame(services)
    df = df.set_index('id')
    df['create_time'] = datetime.datetime.now()
    return df


if __name__ == '__main__':
    df_services = service(200)
    df_services.to_sql('service',engine,if_exists='replace')