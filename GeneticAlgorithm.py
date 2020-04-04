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


def next_generation(data, generation, crossover_rate, mutation_rate):
    # # Breed and mutate children
    # children = breedPopulation(generation, eliteSize)
    # children = mutatePopulation(children, 0.1, mutationRate)
    #
    # # Sum this generation with children
    # generetionSum = generation + children
    #
    # # Rank every individual
    # ranked = rankPaths(graph, generetionSum)
    #
    # # Select individuals for next generation
    # selected = selection(ranked, eliteSize, len(generation))
    #
    # # Get individual list from index list
    # nextGen = indexToPopulation(generetionSum, selected)
    #
    # return nextGen
    pass


def breed_population(mating_pool, elite_size, crossover_rate):
    pass


def mutate_population(population, selection_rate, mutation_rate):
    pass


def init_population(pop_size, data, heuristic_ratio=0.03):
    """
    Populate the initial population with
    solutions found by heuristic and random ones.
    Heuristic solutions make some of total solutions in the population.
    :param pop_size: Size of population
    :param data: Input data
    :param heuristic_ratio: Heuristic solutions/all solutions
    :return: Initialized population
    """

    heuristic_solutions_number = int(heuristic_ratio * pop_size)
    random_solutions_number = pop_size - heuristic_solutions_number
    population = []

    # Generate heuristic solutions
    # probability of whether item will be chosen is based on profit/weight ratio
    chances_to_choose = [ratio/max(data['ratios']) for ratio in data['ratios']]
    for _ in range(heuristic_solutions_number):
        weight_sum = 0
        solution = [0]*data['n']
        for i, chance in enumerate(chances_to_choose):
            if weight_sum + data['weights'][i] <= data['capacity']:
                if random.random() < chance:
                    solution[i] = 1
                    weight_sum += data['weights'][i]
        population.append(solution)

    # Generate random solutions
    for _ in range(random_solutions_number):
        population.append(gen_random_chromosome(data['n']))

    return population


def gen_random_chromosome(size) -> list:
    return [random.randint(0, 1) for _ in range(size)]


def mutate(chromosome):
    """
    Select and flip random bit in chromosome
    :param chromosome: Chromosome to mutate
    :return: Mutated chromosome
    """
    idx = random.randint(0, len(chromosome)-1)
    mutated = chromosome.copy()
    mutated[idx] = 1 - chromosome[idx]
    return mutated
