import random

from deap import tools

random.seed(0)

x = random.sample(range(10), 10)
print(x)
print(tools.mutShuffleIndexes(x, 1))
print(x)

ind1 = random.sample(range(10), 10)
ind2 = random.sample(range(10), 10)

tools.cxTwoPoint(ind1, ind2)
ind = [ind1, ind2]

tools.cxOrdered(ind1, ind2)

for i in range(100):
    ind1 = random.sample(range(10), 10)
    ind2 = random.sample(range(10), 10)
    tools.mutShuffleIndexes(ind1, 1)
    print(ind1)

for i in range(100):
    ind1 = random.sample(range(10), 10)
    tools.mutUniformInt(ind1, 20, 100, 1)
    print(ind1)

for i in range(100):
    ind1 = random.sample(range(100), 10)
    ind2 = random.sample(range(100), 10)
    tools.cxPartialyMatched(ind1, ind2)
    print(ind1)
    print(ind2)
    print(len(set(ind1)),len(set(ind2)))


while True:
    ind1 = random.sample(range(100), 10)
    ind2 = random.sample(range(100), 10)
    # print(ind1, ind2)
    # print(len(set(ind1)), len(set(ind2)))
    if len(set(ind1)) != len(set(ind2)):
        print(len(set(ind1)), len(set(ind2)))
    tools.cxTwoPoint(ind1, ind2)



