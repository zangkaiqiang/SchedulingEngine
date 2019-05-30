import pandas as pd

from engine.engine import engine

df = pd.read_sql("select * from greedy", engine)

# delay
delay = df.delay.sum()
print("The sum delay minutes: %d\n" % delay)

# fair
df_avg = df[['time', 'worker']].groupby(['worker'], as_index=False).sum()
avg_time = df_avg.time.mean()
df_avg['time_diff'] = df_avg['time'] - avg_time
print('*' * 40)
print(df_avg)
print('*' * 40)

print("avg work time: %d" % avg_time)

abs_diff = abs(df_avg['time_diff']).sum()
print("L1 difference: %d" % abs_diff)
