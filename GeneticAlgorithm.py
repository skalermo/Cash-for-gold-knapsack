import random
from datetime import datetime


def crossover(parents, seed=None, point=None):
    """
    Single point crossover.
    Produce two offsprings, each carrying some genetic information from both parents.

    (If point is set, seed has no effect on choosing crossover point)

    :param parents: Chromosome pair
    :param seed:    Random seed
    :param point:   Crossover point
    :return:
    """
    chromosome1, chromosome2 = parents

    # Set seed
    if seed is None:
        seed = datetime.now().microsecond
    random.seed(seed)

    # Choose crossover point
    if point is None:
        point = random.randint(0, len(chromosome1) - 1)

    # Cross genes
    child1 = chromosome1[:point] + chromosome2[point:]
    child2 = chromosome2[:point] + chromosome1[point:]

    return child1, child2




