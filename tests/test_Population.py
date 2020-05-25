import unittest
from Generator import gen_data
from GeneticAlgorithm import init_population


class TestPopulation(unittest.TestCase):
    def test_init_population_size(self):
        data = gen_data()
        population = init_population(100, data, 'vanilla')
        self.assertEqual(100, len(population))


if __name__ == '__main__':
    unittest.main()
