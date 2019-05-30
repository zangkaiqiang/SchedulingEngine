import random
import datetime
import multiprocessing

import pandas as pd
import numpy as np
from deap import creator
from deap import base
from deap import tools
from deap import algorithms

from engine.engine import engine

df_service = pd.read_sql('select id, earliest, latest, time from service', engine)
df_worker = pd.read_sql('select * from worker limit 5', engine)


# 评估方法
def evaluate(individual):
    df = df_service.copy()

    df['order'] = individual[0]
    worker = np.zeros(len(df))
    for i in range(len(individual[1])):
        worker[individual[1][i]:] = i + 1
    df['worker'] = worker
    df = df.sort_values(['worker', 'order'])

    # 添加超时
    delay = evaluate_delay(df)

    # 添加照护员平均
    worker_avg = evaluate_avg(df)

    return delay, worker_avg


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


# 定义新的混合进化模式，不同的基因组选择不同的策略
def mixed_mate(ind1, ind2):
    tools.cxPartialyMatched(ind1[0], ind2[0])
    tools.cxTwoPoint(ind1[1], ind2[1])
    return ind1, ind2


# 定义混合突变模式，不同的基因可以采用不同的突变
def mixed_mutate(individual, indpb):
    tools.mutShuffleIndexes(individual[0], indpb)
    tools.mutUniformInt(individual[1], 1, len(df_service) - 1, 0.2)
    return individual,


# 存储结果
def store(hof):
    df = df_service.copy()
    df['order'] = hof[0]
    worker = np.zeros(len(df))
    for i in range(len(hof[1])):
        worker[hof[1][i]:] = i + 1
    df['worker'] = worker
    df = df.sort_values(['worker', 'order'])
    df['create_time'] = datetime.datetime.now()
    df.to_sql('ga_scheduling', engine, if_exists='replace', index=False)


def ga(core_num, pop_num, n):
    random.seed(11)

    # 定义类型
    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    # 添加多个基因
    toolbox.register('indices', random.sample, range(len(df_service)), len(df_service))
    toolbox.register('cutting', random.sample, range(1, len(df_service) - 1), len(df_worker) - 1)

    # 定义初始化种群方法
    toolbox.register('individual', tools.initCycle, creator.Individual, (toolbox.indices, toolbox.cutting))
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    # 添加配对，变异，择优
    toolbox.register("mate", mixed_mate)
    toolbox.register("mutate", mixed_mutate, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluate)

    pool = multiprocessing.Pool(processes=core_num)
    toolbox.register("map", pool.map)

    # 初始化种群
    population = toolbox.population(n=pop_num)

    # 保存最有结果
    hof = tools.HallOfFame(1)

    # 添加统计指标
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    # 迭代
    algorithms.eaSimple(population, toolbox, 0.7, 0.2, n, stats=stats, halloffame=hof)

    return population, stats, hof


def run():
    p, s, h = ga(8, 300, 500)
    store(h[0])


if __name__ == '__main__':
    run()
