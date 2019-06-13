import pandas as pd

from engine.engine import engine


# 删除一个工单 是否重排
def delete(id):
    df = pd.read_sql('select * from greedy', engine)

    worker_id = df.loc[df.id == id].worker.iloc[0]
    df = df.loc[df.id != id]
    df_worker = df[df.worker == worker_id].copy()

    # df_worker['actual_start'] = df['earliest']
    # df_worker['actual_end'] = df['actual_start'] + df['time']
    start = df_worker['earliest'].tolist()
    end = (df_worker['actual_start'] + df_worker['time']).tolist()
    used_time = df_worker['time'].tolist()
    for i, j in zip(range(len(df_worker) - 1), range(1, len(df_worker))):
        if start[j] < end[i]:
            start[j] = end[i]
            end[j] = start[j] + used_time[j]

    df_worker['actual_start'] = start
    df_worker['actual_end'] = end

    df = df[df.worker != worker_id]
    df = df.append(df_worker)

    df.to_sql('greedy_update', engine, if_exists='replace')


def add(task, org_id, staff_id):
    # 添加task为指定员工
    tasks = get_tasks(org_id, staff_id)
    tasks_adjust = need_adjust_tasks(task, tasks)
    tasks_adjust = adjust_task(task, tasks_adjust)

    tasks = update_task(task, tasks, tasks_adjust)

    return tasks


def get_tasks(org_id, staff_id):
    # get all tasks

    return 0


def need_adjust_tasks(task, tasks):
    # 找到需要在task后执行的tasks

    return 0


def adjust_task(task, tasks_adjust):
    # 调整task后执行的tasks

    return 0


def update_task(task, tasks, tasks_adjust):
    # 将调整过的tasks_adjust更新如tasks

    return tasks


if __name__ == '__main__':
    delete(141)
