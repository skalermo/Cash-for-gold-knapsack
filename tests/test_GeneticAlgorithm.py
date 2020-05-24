import unittest
from Chromosome import Chromosome
from Generator import gen_data
from GeneticAlgorithm import init_population, genetic_algorithm
from BNBAlgorithm import knapsack
import matplotlib.pyplot as plt


class TestGeneticAlgorithm(unittest.TestCase):
    def test_ga(self):
        data = gen_data(100, capacity_type='average', seed=0)
        # print(knapsack(data))
        ga = genetic_algorithm(data, 300, seed=0)
        for _ in range(300):
            next(ga)
        results = next(ga)
        for c in results[0]:
            c.repair('greedy')
        print(results[0][0].fitness)
        print(results[0][0].weight_sum)
        print(data['capacity'])
        print(results[0][0].is_overfilled())
        print(results[0][0].decode())
        print(data['weights'])
        print(data['profits'])


if __name__ == '__main__':
    unittest.main()
