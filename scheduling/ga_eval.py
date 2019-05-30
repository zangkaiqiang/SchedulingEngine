# 超时计算评估
def evaluate_delay(df):
    # 初始化延迟
    delay = 0

    for w in df.worker.unique():
        df_delay = df[df.worker == w].copy()
        start = list(df_delay['earliest'])
        end = list(df_delay['earliest'] + df_delay['time'])
        service_time = list(df_delay['time'])
        length = len(df_delay)

        # 实际开始开始时间小于上个任务的结束时间时，将该开始时间设置为上个任务的结束时间,并更新该任务的实际结束时间
        for i, j in zip(range(1, length), range(length - 1)):
            if start[i] < end[j]:
                start[i] = end[j]
                end[i] = start[i] + service_time[i]

        df_delay['actual_start'] = start
        df_delay['actual_end'] = end

        # 计算超时时间: 最迟-实际开始
        df_delay['delay'] = df_delay['actual_start'] - df_delay['latest']
        df_delay.loc[df_delay.delay < 0, 'delay'] = 0
        delay = delay + df_delay['delay'].sum()

    return delay


# 方差评估
def evaluate_avg(df_):
    df = df_.copy()
    df = df[['worker', 'time']].groupby(['worker'], as_index=False).sum()
    return df.time.std()

