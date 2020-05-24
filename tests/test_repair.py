import unittest
from Generator import gen_data
from Chromosome import Chromosome
from GeneticAlgorithm import init_population


class TestRepairChromosome(unittest.TestCase):
    def test_no_overfilling(self):
        data = gen_data(seed=0)
        c = Chromosome([0]*data['n'], data)
        c[0] = 1
        weight_sum = data['weights'][0]
        self.assertLessEqual(weight_sum, data['capacity'])

    def test_no_overfilling_repair(self):
        data = gen_data(seed=0)
        c = Chromosome([0] * data['n'], data)
        c[0] = 1
        weight_sum = data['weights'][0]
        copied = c.copy()
        c.repair()
        self.assertEqual(copied.gene, c.gene)
        self.assertLessEqual(weight_sum, data['capacity'])

    def test_greedy_repair(self):
        data = gen_data(n=10, capacity=1, seed=0)
        c = Chromosome([1]*10, data)
        self.assertGreater(c.weight_sum, data['capacity'])

        copied = c.copy()
        c.repair()
        self.assertNotEqual(copied.gene, c.gene)
        weight_sum = sum([c.gene[i] * data['weights'][i] for i in range(len(c.gene))])
        self.assertLessEqual(weight_sum, data['capacity'])


if __name__ == '__main__':
    unittest.main()
