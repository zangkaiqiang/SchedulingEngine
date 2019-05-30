import argparse

from scheduling.ga_scheduling import ga
from scheduling.ga_scheduling import store

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('--cores', type=int, help='cpu cores')
    parser.add_argument('--pop', type=int, help='pop numbers')
    parser.add_argument('--numbers', type=int, help='iter numbers')

    args = parser.parse_args()

    p, s, h = ga(args.cores, args.pop, args.numbers)
    store(h[0])
