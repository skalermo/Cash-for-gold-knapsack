import random
from datetime import datetime
import numpy as np


def crossover(parents, seed=None, point=None):
    """
    Single point crossover.
    Produce two offsprings, each carrying some genetic information from both parents.

    (If point is set, seed has no effect on choosing crossover point)

    :param parents: Chromosome pair
    :param seed:    Random seed
    :param point:   Crossover point
    :return:        2 children
    """
    x, y = parents

    # Set seed
    if seed is None:
        seed = datetime.now().microsecond
    random.seed(seed)

    # Choose crossover point
    if point is None:
        point = random.randint(0, len(x) - 1)

    # Cross genes
    child1 = x[:point] + y[point:]
    child2 = y[:point] + x[point:]

    return child1, child2


def fitness(x, data, has_penalty=False):
    """
    Fitness evaluation function with logarithmic penalty function

    :param x:           Solution to the problem
    :param data:        Dictionary with weights, capacity and profits
    :param has_penalty: Boolean. If True - use penalty function
    :return:            Fitness evaluation
    """
    penalty = 0
    if has_penalty:
        # Find p = max(P[i] / W[i]) and weight_sum = sum(x[i] * W[i] - C)
        p = 0
        weight_sum = 0
        for i in range(len(x)):
            weight_sum += x[i] * data['weights'][i] - data['capacity']

            ratio = data['profits'][i] / data['weights'][i]
            if ratio > p:
                p = ratio

        penalty = np.log2(1 + p * weight_sum)

    # Find fitness = sum(x[i] * P[i] - Penalty(x))
    fit = 0
    for i in range(len(x)):
        fit += x[i] * data['profits'][i] - penalty

    return fit



