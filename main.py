import argparse
from BNBAlgorithm import knapsack as BNBAlgorithm
from Generator import gen_data

algorithms = {
    'bnb': BNBAlgorithm,
    'genetic': None,
    'modified': None
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='main.py', description='Knapsack 0/1 (Cash for Gold)')
    parser.add_argument('-s', type=float, default=None, metavar='', help='Seed for generator')
    parser.add_argument('-n', type=int, default=100, metavar='', help='Number of items')
    parser.add_argument('-v', type=int, default=10, metavar='', help='Weight cap')
    parser.add_argument('-r', type=int, default=5, metavar='', help='Correlation value')
    parser.add_argument('-p', type=str, default='weak', metavar='',
                        help='Correlation between profits and weights (none, weak, strong)')
    parser.add_argument('-c', type=str, default='average', metavar='',
                        help='Capacity type (restrictive, average, custom: number)')
    parser.add_argument('-a', type=str, metavar='', help='Algorithm type (BnB, Genetic, Modified)')
    parser.add_argument('-d', type=int, default=None, help='Depth for BnB Algorithm')
    parser.add_argument('-g', type=int, default=100, metavar='', help='Number of generations')

    args = vars(parser.parse_args())

    # Check selected algorithm
    if args['a'] is None:
        parser.print_help()
        exit(1)

    selected_algorithm = args['a'].lower()

    # Set seed
    seed = args['s']

    # Prepare args for generator
    if args['c'].isnumeric():
        capacity = int(args['c'])
        capacity_type = 'custom'
    else:
        capacity = None
        capacity_type = args['c'].lower()

    gen_args = (args['n'], args['v'], args['r'], args['p'], capacity, capacity_type, seed)

    # Generate data
    data = gen_data(*gen_args)

    # Start algorithm
    if selected_algorithm == 'bnb':
        func_args = (data, args['d'])
    else:
        func_args = (data,)

    result = algorithms[selected_algorithm](*func_args)

    print(result)
