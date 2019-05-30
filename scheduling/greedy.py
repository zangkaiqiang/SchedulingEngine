import datetime

import pandas as pd

from engine.engine import engine

df_service = pd.read_sql('select id, earliest, latest, time from service', engine)
df_worker = pd.read_sql('select * from worker limit 5', engine)


df_service = df_service.sort_values(['earliest'])
df_service['actual_start'] = None
df_service['actual_end'] = None

df_worker['end'] = 0
worker = []
actual_start = []
for i in range(len(df_service)):
    df_worker = df_worker.sort_values(['end'])
    worker.append(df_worker.id.iloc[0])
    service_start = df_service.earliest.iloc[i]
    work_end = df_worker.end.iloc[0]
    actual_start.append(max(service_start, work_end))
    df_worker.loc[df_worker.id == worker[i], 'end'] = actual_start[i] + df_service.time.iloc[i]

df_service['actual_start'] = actual_start
df_service['worker'] = worker
df_service['actual_end'] = df_service['actual_start'] + df_service['time']
df_service['delay'] = df_service['actual_start'] - df_service['latest']
df_service.loc[df_service.delay < 0, 'delay'] = 0
df_service['create_time'] = datetime.datetime.now()
df_service.to_sql('greedy', engine, if_exists='replace', index=False)
