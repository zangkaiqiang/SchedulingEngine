import pandas as pd

from engine.engine import engine

df = pd.read_sql('select * from ga_scheduling', engine)


def add_delay(df_):
    df = df_.copy()
    start = list(df.earliest)
    end = list(df.earliest + df.time)
    service_time = list(df.time)

    length = len(df)

    # 实际开始开始时间小于上个任务的结束时间时，将该开始时间设置为上个任务的结束时间,并更新该任务的实际结束时间
    for i, j in zip(range(1, length), range(length - 1)):
        if start[i] < end[j]:
            start[i] = end[j]
            end[i] = start[i] + service_time[i]

    df['actual_start'] = start
    df['actual_end'] = end

    # 计算超时时间: 最迟-实际开始
    df['delay'] = df['actual_start'] - df['latest']
    df.loc[df.delay < 0, 'delay'] = 0

    return df


df_delay = pd.DataFrame()
for i in df.worker.unique():
    df_delay = df_delay.append(add_delay(df[df.worker == i]))


def judge(df_):
    # delay
    df = df_.copy()
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


judge(df_delay)
