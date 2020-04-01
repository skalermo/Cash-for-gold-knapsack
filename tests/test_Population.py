import unittest
from Generator import gen_data
from GeneticAlgorithm import init_population, fitness


class TestPopulation(unittest.TestCase):
    def test_init_population_size(self):
        data = gen_data()
        population = init_population(100, data)
        self.assertEqual(100, len(population))

        population = init_population(100, data, heuristic_ratio=0)
        self.assertEqual(100, len(population))

        population = init_population(100, data, heuristic_ratio=0.3)
        self.assertEqual(100, len(population))

        population = init_population(100, data, heuristic_ratio=1)
        self.assertEqual(100, len(population))

    def test_init_population_heuristic_solutions(self):
        data = gen_data()
        population = init_population(100, data, heuristic_ratio=0.34)
        n = int(0.34*100)
        self.assertTrue(all([fitness(solution, data) > 0 for solution in population[:n]]))


if __name__ == '__main__':
    unittest.main()
