import argparse
import json
import random
from datetime import datetime


def gen_data(n: int = 100,
             v: int = 10,
             r: int = 5,
             correlation: str = 'weak',
             capacity: float = None,
             capacity_type: str = 'restrictive',
             seed: int = None
             ) -> dict:
    """
    Generate data according to formulas:
    (W stands for weights, P - for profits, C - for capacity)

    correlation: none
        W[i] := (uniformly) random(1..v)
        P[i] := (uniformly) random(1..v)

    correlation: weak
        W[i] := (uniformly) random(1..v)
        P[i] := W[i] + (uniformly) random(-r..r)
        if P[i] < 0: repeat prev line until P[i] > 0

    correlation: strong
        W[i] := (uniformly) random(1..v)
        P[i] := W[i] + r

    capacity_type: restrictive
        C = 2v

    capacity_type: average
        C = 0.5 * sum(W)

    :param n: Number of items
    :param v: Weight cap
    :param r: Correlation value
    :param correlation: Correlation between profits and weights
    :param capacity: Set capacity explicitly
    :param capacity_type: Restrictive, average or random
    :param seed: Random seed
    :return: Dictionary with generated data
    """

    # set seed
    if seed is None:
        seed = datetime.now().microsecond
    random.seed(seed)

    weights = [round(random.uniform(1, v), 1) for _ in range(n)]

    if correlation is None:
        correlation = 'weak'

    profits = []
    if correlation == 'none':
        profits = [round(random.uniform(1, v), 1) for _ in range(n)]
    elif correlation == 'weak':
        profits = _weak_corr_profits(n, r, weights)
    elif correlation == 'strong':
        profits = [round(r + weights[i], 1) for i in range(n)]

    ratios = [p/w for w, p in zip(weights, profits)]

    # get sorted by p/w ratio indices
    sorted_indices = [i[0] for i in sorted(enumerate(ratios), key=lambda x: x[1], reverse=True)]

    if capacity is None:
        capacity = {
            'restrictive': 2*v,
            'average': 0.5*sum(weights),
        }.get(capacity_type, 'restrictive')
    else:
        capacity_type = 'custom'

    data = {
        'n': n,
        'weights': weights,
        'profits': profits,
        'ratios': ratios,
        'sorted_indices': sorted_indices,
        'capacity': capacity,
        'capacity_type': capacity_type,
        'correlation': correlation,
        'seed': seed
    }
    return data


def _weak_corr_profits(n: int, r: float, weights: list) -> list:
    """
    Generate profits weakly correlated to provided weights
    :param n: Number of items
    :param r: Difference cap between weights and profits
    :param weights: Provided list of weights
    :return: List of profits
    """
    profits = []
    for i in range(n):
        profit = -1
        while profit <= 0.0:
            profit = weights[i] + round(random.uniform(-r, r), 1)
        profits.append(profit)
    return profits

if __name__ == '__main__':
    # Parser for generator
    parser = argparse.ArgumentParser(prog='Generator.py', description='Generator for Knapsack 0/1')
    parser.add_argument('-o', '--file', type=str, default=None, metavar='', help='Data file')
    parser.add_argument('-s', '--seed', type=float, default=None, metavar='', help='Seed for generator')
    parser.add_argument('-n', '--items', type=int, default=100, metavar='', help='Number of items')
    parser.add_argument('-v', '--weight', type=int, default=10, metavar='', help='Weight cap')
    parser.add_argument('-r', '--value', type=int, default=5, metavar='', help='Correlation value')
    parser.add_argument('-p', '--correlation', type=str, default='weak', metavar='',
                        help='Correlation between profits and weights (none, weak, strong)')
    parser.add_argument('-c', '--type', type=str, default='average', metavar='',
                        help='Capacity type (restrictive, average, custom: number)')

    args = parser.parse_args()

    # Set seed
    seed = args.seed

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

    if args.file is None:
        print(data)
    else:
        json.dump(data, open(args.file, 'w'), indent=4)
