import pytest

import numpy as np
import pandas as pd

from engine.engine import engine
from simulation_system.service import service
from scheduling.ga_scheduling import evaluate_delay


def test_ga():
    '''

    :return:
    '''


def test_delay():
    '''

    :return:
    '''
    df = service(100)
    df['worker'] = np.random.randint(2, size=100)
    delay = evaluate_delay(df)

    assert delay > 0


def get_delay(order):
    df = pd.read_sql('select earliest,latest,time from service limit 10', engine)

    df['order'] = order
    df = df.sort_values(['order'])

    df_eval = df.copy()
    # 初始化实际开始时间和结束时间为预定的开始时间和结束时间
    df_eval['actual_start'] = df_eval['earliest']
    df_eval['actual_end'] = df_eval['earliest'] + df_eval['time']

    # 实际开始开始时间小于上个任务的结束时间时，将该开始时间设置为上个任务的结束时间,并更新该任务的实际结束时间
    for i in range(len(df_eval) - 1):
        last_end = df_eval.actual_end.iloc[i]
        start = df_eval.actual_start.iloc[i + 1]
        if start < last_end:
            df_eval['actual_start'].iloc[i + 1] = last_end
            df_eval['actual_end'].iloc[i + 1] = last_end + df_eval.time.iloc[i + 1]

    # 计算超时时间: 最迟-实际开始
    df_eval['delay'] = df_eval['actual_start'] - df_eval['latest']
    df_eval.loc[df_eval.delay < 0, 'delay'] = 0
    print(df_eval.delay.sum())


if __name__ == '__main__':
    test_ga()
