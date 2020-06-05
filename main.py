import argparse
import json

from BNBAlgorithm import knapsack
from GeneticAlgorithm import genetic_algorithm
from Generator import gen_data


def BnB_Algorithm(args):
    print('BnB algorithm')
    return knapsack(*args)


def Genetic_Algorithm(args, generations):
    print('Genetic algorithm for {} generations'.format(generations))

    algorithm = genetic_algorithm(*args)

    for _ in range(generations - 1):
        next(algorithm)
    population = next(algorithm)

    best_chromo = population[0]
    best_chromo.repair()
    best_chromo.calc_fitness(args[1] == 'penalty')

    result = {'profits': best_chromo.fitness, 'optimal': best_chromo.gene,
              'weight': best_chromo.weight_sum}

    return result


algorithms = {
    'bnb': BnB_Algorithm,
    'genetic': Genetic_Algorithm,
}
if __name__ == '__main__':
    # Parser for generator
    parser = argparse.ArgumentParser(prog='main.py', description='Knapsack 0/1 (Cash for Gold)')
    parser.add_argument('-i', '--file', type=str, default=None, metavar='', help='Data file')
    parser.add_argument('-s', '--seed', type=float, default=None, metavar='', help='Seed for generator')
    parser.add_argument('-n', '--items', type=int, default=100, metavar='', help='Number of items')
    parser.add_argument('-v', '--weight', type=int, default=10, metavar='', help='Weight cap')
    parser.add_argument('-r', '--value', type=int, default=5, metavar='', help='Correlation value')
    parser.add_argument('-p', '--correlation', type=str, default='weak', metavar='',
                        help='Correlation between profits and weights (none, weak, strong)')
    parser.add_argument('-c', '--type', type=str, default='average', metavar='',
                        help='Capacity type (restrictive, average, custom: number)')

    # Subparsers for algorithms
    subparsers = parser.add_subparsers(dest='algorithms')

    # Arguments for BnB
    bnb_parser = subparsers.add_parser('bnb')
    bnb_parser.add_argument('-d', '--depth', type=int, default=None, metavar='', help='Depth for BnB Algorithm')

    # Arguments for Genetic
    genetic_parser = subparsers.add_parser('genetic')
    genetic_parser.add_argument('-g', '--generations', type=int, default=100, metavar='', help='Number of generations')
    genetic_parser.add_argument('-m', '--method', type=str, default='vanilla', metavar='',
                                help='Genetic algorithm method(vanilla, repair, penalty)')
    genetic_parser.add_argument('-p', '--pop_size', type=int, default=100, metavar='', help='Population size')
    genetic_parser.add_argument('-c', '--crossover', type=float, default=0.65, metavar='', help='Crossover rate')
    genetic_parser.add_argument('-r', '--mutation', type=float, default=0.05, metavar='', help='Mutation rate')

    args = parser.parse_args()

    # Check selected algorithm
    algorithm = args.algorithms
    if algorithm is None or algorithm not in algorithms:
        parser.print_help()
        exit(0)

    # Set seed
    seed = args.seed

    if args.file is None:
        # Prepare args for generator
        if args.type.isnumeric():
            capacity = int(args.type)
            capacity_type = 'custom'
        else:
            capacity = None
            capacity_type = args.type.lower()

        gen_args = (args.items, args.weight, args.value, args.correlation, capacity, capacity_type, seed)

        # Generate data
        data = gen_data(*gen_args)
    else:
        try:
            data = json.load(open(args.file, 'r'))
        except FileNotFoundError:
            print('File {} not found'.format(args.file))
            exit(0)

    # Start algorithm
    if algorithm == 'bnb':
        func_args = (data, args.depth)
        result = algorithms[algorithm](func_args)
    elif algorithm == 'genetic':
        func_args = (data, args.method, args.pop_size, args.crossover, args.mutation, seed)
        result = algorithms[algorithm](func_args, args.generations)

    print(result)
