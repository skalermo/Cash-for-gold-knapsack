import unittest
from Chromosome import Chromosome
from Generator import gen_data
from GeneticAlgorithm import init_population, genetic_algorithm
from BNBAlgorithm import knapsack
import matplotlib.pyplot as plt


class TestGeneticAlgorithm(unittest.TestCase):
    def test_ga(self):
        data = gen_data(100, correlation='strong', capacity_type='average', seed=0)
        # print(knapsack(data))
        results = genetic_algorithm(data, 300, seed=0)
        plt.plot(results[1], 'blue')
        plt.plot(results[2], 'red')
        plt.show()
        print(results[0].fitness)
        print(results[0].weight_sum)
        print(data['capacity'])
        print(results[0].is_overfilled())
        print(results[0].decode())
        print(data['weights'])
        print(data['profits'])


if __name__ == '__main__':
    unittest.main()
