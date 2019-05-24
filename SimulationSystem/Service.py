'''
服务模拟
'''
import pandas as pd
from random import randint
import random
random.seed(0)

def service(num):
    services = []
    for i in range(num):
        dict = {}
        dict['id'] = i
        dict['senior_id'] = randint(1,10)
        dict['time'] = randint(10,100)
        dict['start'] = randint(0,12*60)
        services.append(dict)
    return services

if __name__ == '__main__':
    service(100)