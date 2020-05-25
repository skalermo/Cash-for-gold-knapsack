import os
import json


import GeneticAlgorithm
import BNBAlgorithm
import Generator
import Chromosome


def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


if __name__ == '__main__':

    dirname = './logs/'
    makedir(dirname)

    for no_of_items in [100, 250, 500]:
        for capacity_type in ['restrictive', 'average']:
            for correlation in ['none', 'weak', 'strong']:
                data = Generator.gen_data(n=no_of_items,
                                          capacity_type=capacity_type,
                                          correlation=correlation)

                optimal_solution = None
                if capacity_type != 'average':
                    optimal_solution = BNBAlgorithm.knapsack(data)

                for method in ['vanilla', 'repair', 'penalty']:
                    algorithm = GeneticAlgorithm.genetic_algorithm(data, method=method)

                    results = {
                        'vars': [no_of_items, capacity_type, correlation, method, data['seed']],
                        'optimal': optimal_solution,
                        'fitness': [],
                        'fitness_avg': [],
                        'best_fitness': 0,
                        'best_gene': None
                    }

                    print(*results['vars'])
                    for i in range(500):
                        population = next(algorithm)
                        sum = 0

                        for chromosome in population:
                            chromosome.repair('greedy')
                            chromosome.calc_fitness(True)
                            sum += chromosome.fitness
                            if results['best_fitness'] < chromosome.fitness:
                                results['best_fitness'] = chromosome.fitness
                                results['best_gene'] = chromosome.gene[:]
                        results['fitness'].append(population[0].fitness)
                        results['fitness_avg'].append(sum / len(population))
                    filename = f'{no_of_items}_{capacity_type}_{correlation}_{method}'
                    with open(dirname + filename, 'w') as f:
                        json.dump(results, f, indent=2)
                        f.flush()
                    print(*results['vars'], 'Done.')


