import random
import pandas as pd
import numpy as np

from deap import creator
from deap import base
from deap import tools
from deap import algorithms

from engine.engine import engine

df_service = pd.read_sql('select earliest,latest,time from service limit 100', engine)
df_worker = pd.read_sql('select * from worker limit 5', engine)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create('Individual', list, fitness=creator.FitnessMin)

creator.create("FitnessMinGroup", base.Fitness, weights=(-1.0,))
creator.create("IndividualGroup", list, fitness=creator.FitnessMinGroup)

toolbox = base.Toolbox()


def gen_indices(service_length, worker_length):
    service_list = random.sample(range(service_length), service_length)
    cutting_points = random.sample(range(service_length), worker_length - 1)

    return service_list


def worker_service(service_list, cutting_points):
    cutting_points.sort()
    worker_services = []
    for i, j in zip(cutting_points[0:-1], cutting_points[1:]):
        worker_services.append(service_list[i:j])
    worker_services.append(service_list[:cutting_points[0]])
    worker_services.append(service_list[cutting_points[-1]:])

    return worker_services


toolbox.register('indices', random.sample, range(len(df_service)), len(df_service))
toolbox.register('cutting', random.sample, range(len(df_service)), len(df_worker))
toolbox.register('individual', tools.initCycle, creator.Individual, (toolbox.indices, toolbox.cutting))
toolbox.register('population', tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
    service_mat = worker_service(individual[0], individual[1])
    df_eval = df_service.copy()

    # 初始化实际开始时间和结束时间为预定的开始时间和结束时间
    df_eval['actual_start'] = df_eval['earliest']
    df_eval['actual_end'] = df_eval['earliest'] + df_eval['time']

    df_result = pd.DataFrame()

    for atom in service_mat[:]:
        df_eval_worker = df_eval[df_eval.index.isin(atom)].copy()
        df_eval_worker = add_delay(df_eval_worker, atom)
        df_result = df_result.append(df_eval_worker)

    df_result.loc[df_result.delay < 0, 'delay'] = 0

    return df_result.delay.sum(),


def add_delay(df_eval_worker, atom):
    df_eval_worker['order'] = atom[:]
    df_eval_worker = df_eval_worker.sort_values(['order'])

    # 实际开始开始时间小于上个任务的结束时间时，将该开始时间设置为上个任务的结束时间,并更新该任务的实际结束时间
    for i in range(len(df_eval_worker) - 1):
        last_end = df_eval_worker.actual_end.iloc[i]
        start = df_eval_worker.actual_start.iloc[i + 1]
        if start < last_end:
            df_eval_worker['actual_start'].iloc[i + 1] = last_end
            df_eval_worker['actual_end'].iloc[i + 1] = last_end + df_eval_worker.time.iloc[i + 1]

    # 计算超时时间: 最迟-实际开始
    df_eval_worker['delay'] = df_eval_worker['actual_start'] - df_eval_worker['latest']

    return df_eval_worker


toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)


def run():
    random.seed(11)
    pop = toolbox.population(n=300)

    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 10, stats=stats, halloffame=hof)

    return pop, stats, hof


if __name__ == '__main__':
    pop, stats, hof = run()
