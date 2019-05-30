import argparse

from scheduling.ga_scheduling import ga
from scheduling.ga_scheduling import store

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('--cores', type=int, help='cpu cores', default=8)
    parser.add_argument('--mu', type=int, help='pop numbers', default=100)
    parser.add_argument('--ngen', type=int, help='iter numbers', default=100)

    args = parser.parse_args()

    p, s, h = ga(args.cores, args.mu, args.ngen)
    store(h[0])
