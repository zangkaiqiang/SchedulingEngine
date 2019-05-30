import argparse

from scheduling.ga_scheduling import ga
from scheduling.ga_scheduling import store

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('--cores', type=int, help='cpu cores')
    parser.add_argument('--mu', type=int, help='pop numbers')
    parser.add_argument('--ngen', type=int, help='iter numbers')

    args = parser.parse_args()

    p, s, h = ga(args.cores, args.mu, args.ngen)
    store(h[0])
