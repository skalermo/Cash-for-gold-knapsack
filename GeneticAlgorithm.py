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
        weight_sum = sum([x[i] * data['weights'][i] for i in range(len(x))])
        if weight_sum > data['capacity']:
            # Find p = max(P[i] / W[i])
            p = max(data['profits'][i] / data['weights'][i] for i in range(len(x)))

            # Find weight_sum = sum(x[i] * W[i]) - C
            weight_sum -= data['capacity']

            # Set penalty
            penalty = np.log2(1 + p * weight_sum)

    # Find fitness = sum(x[i] * P[i] - Penalty(x))
    return sum([x[i] * data['profits'][i] - penalty for i in range(len(x))])


def genetic_algorithm(data, generations, pop_size=100, crossover_rate=0.65, mutation_rate=0.05, seed=None):
    # Set seed
    if seed is None:
        seed = datetime.now().microsecond
    random.seed(seed)

    # Initialize population
    population = init_population(pop_size, data)
    pass


def next_generation(data, population, crossover_rate=0.65, mutation_rate=0.05, elite_size=1):

    # Select and breed parents
    parents = selection(population, elite_size, 100) # selection size ?
    children = breed(parents, crossover_rate)

    # Mutate parents and children
    new_individuals = parents + children
    mutate_chromosomes(new_individuals, mutation_rate)

    # repair_chromosomes(new_individuals)

    # Sort chromosomes by their fitness
    new_population = sorted(new_individuals, key=lambda x: fitness(x, data, True), reverse=True)

    # Truncate new population size and return new population
    return new_population[:len(population)]


def selection(population, elite_size, selection_size):
    """
    Select parents for next population using Elitism and Tournament Selection
    """

    # Create list and choose elite
    selected = population[:elite_size]

    # Tournament selection
    for _ in range(selection_size - elite_size):
        chromo1_idx, chromo2_idx = random.choices(range(len(population)), k=2)
        idx = min(chromo1_idx, chromo2_idx)
        selected.append(population[idx])

    return selected


def breed(mating_pool, crossover_rate):
    """
    Produce children from elite and by breeding.
    mating_pool is shuffled by this function.
    """

    children = []

    # shuffle mating pool
    random.shuffle(mating_pool)

    # breed new and add them to children
    for i in range(len(mating_pool)//2):
        if random.random() < crossover_rate:
            born_children = crossover(mating_pool[i], mating_pool[-i - 1])
            children.append(*born_children)

    return children


def mutate_chromosomes(chromosomes, mutation_rate):
    for chromosome in chromosomes:
        if random.random() < mutation_rate:
            mutate(chromosome)


def init_population(pop_size, data, heuristic_ratio=0):
    """
    Populate the initial population
    with random solutions.
    Heuristic ratio defines how many chromosomes have first bit set.
    Half of that amount also have last bit unset.
    :param pop_size: Size of population
    :param data: Input data
    :param heuristic_ratio: Heuristic solutions/all solutions
    :return: Initialized population
    """

    heuristic_solutions_number = int(heuristic_ratio * pop_size)
    population = []

    # Generate random solutions
    for _ in range(pop_size):
        population.append(gen_random_chromosome(data['n']))

    # Set first bit
    ids = random.sample(range(pop_size), heuristic_solutions_number)
    for idx in ids:
        population[idx][0] = 1

    # Unset last bit
    ids = random.sample(range(pop_size), heuristic_solutions_number//2)
    for idx in ids:
        population[idx][-1] = 0

    return population


def gen_random_chromosome(size) -> list:
    return [random.randint(0, 1) for _ in range(size)]


def mutate(chromosome):
    """
    Select and flip random bit in chromosome
    :param chromosome: Chromosome to mutate
    """
    idx = random.randint(0, len(chromosome)-1)
    chromosome[idx] = 1 - chromosome[idx]
