# creator: kai

import random
import pandas as pd
import numpy as np

from deap import creator
from deap import base
from deap import tools
from deap import algorithms

from engine.engine import engine

df = pd.read_sql('select earliest,latest,time from service', engine)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register('indices', random.sample, range(len(df)), len(df))

toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)


def evaluate(indivdual):
    df_eval = df.copy()
    df_eval['order'] = indivdual[:]
    df_eval = df_eval.sort_values(['order'])

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
    df_eval['delay'] = df_eval['latest'] - df_eval['actual_start']
    df_eval.loc[df_eval.delay < 0, 'delay'] = 0

    return df_eval.delay.sum(),


toolbox.register("mate", tools.cxPartialyMatched)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)


def run():
    random.seed(11)
    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 400, stats=stats,
                        halloffame=hof)

    return pop, stats, hof


if __name__ == '__main__':
    run()
