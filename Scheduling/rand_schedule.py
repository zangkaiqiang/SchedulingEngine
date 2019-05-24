'''
随机调度
'''
from SimulationSystem import Service,Worker
import pandas as pd
import datetime

import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://kai:vsi666666@localhost/learn?charset=utf8')

worker = Worker.worker(10)
service = Service.service(100)

df_service = pd.DataFrame(service)
df_service = df_service.sort_values(['start'])
df_service['worker'] = None
df_service['actual_start'] = None

