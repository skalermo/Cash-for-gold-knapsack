import random
from datetime import datetime
from Chromosome import Chromosome


def genetic_algorithm(data, pop_size=100, crossover_rate=0.65, mutation_rate=0.05, seed=None):
    # Set seed
    if seed is None:
        seed = datetime.now().microsecond
    random.seed(seed)

    # Initialize population
    population = init_population(pop_size, data)

    progress = population[0].fitness
    progress_avg = sum(chromo.fitness for chromo in population) / len(population)
    yield population, progress, progress_avg

    while True:
        population = next_generation(data, population, crossover_rate, mutation_rate)
        progress = population[0].fitness
        progress_avg = sum(chromo.fitness for chromo in population) / len(population)

        yield population, progress, progress_avg


def next_generation(data, population, crossover_rate=0.65, mutation_rate=0.05, elite_size=1):

    # Select and breed parents
    parents = selection(population, elite_size, 100) # selection size ?
    children = breed(parents, crossover_rate)

    # Mutate parents and children
    new_individuals = parents + children
    mutate_chromosomes(new_individuals, mutation_rate)

    # repair_chromosomes(new_individuals)

    # Sort chromosomes by their fitness
    new_population = sorted(new_individuals, key=lambda x: x.get_fitness(True), reverse=True)

    # Truncate new population size and return new population
    return new_population[:len(population)]


def repair_chromosomes(chromosomes):
    for chromosome in chromosomes:
        chromosome.repair()


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
            born_children = Chromosome.crossover((mating_pool[i], mating_pool[-i - 1],))
            children.extend(born_children)

    return children


def mutate_chromosomes(chromosomes, mutation_rate):
    for chromosome in chromosomes:
        if random.random() < mutation_rate:
            chromosome.mutate()


def init_population(pop_size, data):
    """
    Populate the initial population
    with random solutions.
    :param pop_size: Size of population
    :param data: Input data
    :return: Initialized population
    """

    population = []

    # Generate random solutions
    for _ in range(pop_size):
        population.append(gen_random_chromosome(data))

    for chromo in population:
        chromo.repair(mode='random')
        chromo.get_fitness()

    return population


def gen_random_chromosome(data) -> Chromosome:
    return Chromosome([random.randint(0, 1) for _ in range(data['n'])], data)

