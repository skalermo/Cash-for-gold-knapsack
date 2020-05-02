import unittest
from Generator import gen_data
from GeneticAlgorithm import init_population


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
        hr = 0.3
        data = gen_data()
        population = init_population(50, data, heuristic_ratio=hr)
        first_bits_set_count = 0
        last_bits_unset_count = 0
        for chromosome in population:
            if chromosome[0] == 1:
                first_bits_set_count += 1
            if chromosome[-1] == 0:
                last_bits_unset_count += 1
        self.assertTrue(first_bits_set_count/50 >= hr)
        self.assertTrue(last_bits_unset_count/50 >= hr/2)


if __name__ == '__main__':
    unittest.main()
