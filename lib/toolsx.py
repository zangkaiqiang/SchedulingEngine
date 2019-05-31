import random

from deap import tools

from itertools import repeat
from collections import Sequence


class HallOfFamex(tools.HallOfFame):
    def update(self, population):
        """Update the hall of fame with the *population* by replacing the
        worst individuals in it by the best individuals present in
        *population* (if they are better). The size of the hall of fame is
        kept constant.

        :param population: A list of individual with a fitness attribute to
                           update the hall of fame with.
        """
        if len(self) == 0 and self.maxsize != 0:
            # Working on an empty hall of fame is problematic for the
            # "for else"
            self.insert(population[0])

        for ind in population:
            if sum(ind.fitness.wvalues) < sum(self[-1].fitness.wvalues) or len(self) < self.maxsize:
                for hofer in self:
                    # Loop through the hall of fame to check for any
                    # similar individual
                    if self.similar(ind, hofer):
                        break
                else:
                    # The individual is unique and strictly better than
                    # the worst
                    if len(self) >= self.maxsize:
                        self.remove(-1)
                    self.insert(ind)


# 随机选择
def cx_pick(ind1, ind2):
    '''
    从个体1和个体2的基因中随机选择同样长度的n个属性，保证子孙个体的每个属性也是唯一的
    :param ind1:
    :param ind2:
    :return:
    '''
    ind_set = set(ind1)
    ind_set.union(ind2)
    ind1 = random.sample(ind_set, len(ind1))
    ind2 = random.sample(ind_set, len(ind2))

    return ind1, ind2


#
def mut_uniform_unique(individual, low, up, indpb):
    '''

    :param individual:
    :param low:
    :param up:
    :param indpb:
    :return:
    '''
    size = len(individual)
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))

    for i, xl, xu in zip(range(size), low, up):
        if random.random() < indpb:
            attr = random.randint(xl, xu)
            if attr not in individual:
                individual[i] = attr


