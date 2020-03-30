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

    capacity_type: random
        C = n * avg(W) * random(0..1)

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

    profits = {
        'none': lambda: [round(random.uniform(1, v), 1) for _ in range(n)],
        'weak': lambda: _weak_corr_profits(n, r, weights),
        'strong': lambda: [round(r + weights[i], 1) for i in range(n)]
    }.get(correlation, 'weak')()

    if capacity is None:
        capacity = {
            'restrictive': lambda: 2*v,
            'average': lambda: 0.5*sum(weights),
            'random': lambda: round(random.random()*n*sum(weights)/len(weights), 1)
        }.get(capacity_type, 'restrictive')()
    else:
        capacity_type = 'custom'

    data = {
        'weights': weights,
        'profits': profits,
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
