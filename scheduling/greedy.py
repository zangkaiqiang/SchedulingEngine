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

df_worker = pd.DataFrame(worker)
df_worker['end'] = 0

for i in range(len(df_service)):
    # s = df_service.iloc[i]
    df_worker = df_worker.sort_values(['end'])
    df_service.worker.iloc[i] = df_worker.id.iloc[0]

    service_start = df_service.start.iloc[i]
    work_end = df_worker.end.iloc[0]
    df_service.actual_start.iloc[i] = max(service_start,work_end)
    df_worker.end.iloc[0] = df_service.actual_start.iloc[i]+df_service.time.iloc[i]

df_service['create_time'] = datetime.datetime.now()
df_service.to_sql('greedy',engine,if_exists='replace',index=False)


