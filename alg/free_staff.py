# 工单，单位为秒：100秒-150秒等
task = [[100, 150], [500, 600], [900, 1100]]
# 排班表，单位为秒
shift = [[100, 200], [400, 1000]]

# 预处理，将时间单位分为每秒，存到tasks和shifts
tasks = []
shifts = []
for i in task:
    tasks.extend(list(range(i[0], i[1])))
for i in shift:
    shifts.extend(list(range(i[0], i[1])))

# 取出在排班并且没有做工单的秒
results = []
for i in shifts:
    if i in tasks:
        continue
    results.append(i)

# 将秒连成数组输出
free = []
start = 0
for i in range(len(results) - 1):
    if results[i + 1] - results[i] != 1:
        free.append([results[start], results[i] + 1])
        start = i + 1
free.append([results[start], results[-1] + 1])
print(free)
