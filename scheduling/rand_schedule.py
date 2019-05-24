'''
随机调度
'''
from simulation_system import service,worker
import pandas as pd
import datetime

import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://kai:vsi666666@localhost/learn?charset=utf8')

worker = worker.worker(10)
service = service.service(100)

df_service = pd.DataFrame(service)
df_service = df_service.sort_values(['start'])
df_service['worker'] = None
df_service['actual_start'] = None

