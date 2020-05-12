import unittest
from Chromosome import Chromosome


class TestFitness(unittest.TestCase):
    def setUp(self):
        self.data1 = {'capacity': 10, 'weights': [2, 3.14, 1.98, 5.0, 3.0], 'profits': [40, 50, 100, 95, 30]}
        self.data1['ratios'] = [self.data1['profits'][i] / self.data1['weights'][i] for i in range(len(self.data1))]
        self.optimal1 = Chromosome([1, 0, 1, 1, 0], self.data1)

        self.data2 = {'capacity': 26, 'weights': [12,  7, 11,  8,  9], 'profits': [24, 13, 23, 15, 16]}
        self.data2['ratios'] = [self.data2['profits'][i] / self.data2['weights'][i] for i in range(len(self.data2))]

        self.optimal2 = Chromosome([0, 1, 1, 1, 0], self.data2)

        self.suboptimal1 = Chromosome([1, 1, 1, 1, 1], self.data1)
        self.suboptimal2 = Chromosome([1, 1, 1, 1, 1], self.data2)

    def test_withoutPenalty(self):
        self.assertEqual(235, self.optimal1.get_fitness(has_penalty=False), 'Incorrect fitness for dataset 1')
        self.assertLess(235, self.suboptimal1.get_fitness(has_penalty=False), 'Incorrect fitness for dataset 1')

        self.assertEqual(51, self.optimal2.get_fitness(has_penalty=False), 'Incorrect fitness for dataset 2')
        self.assertLess(51, self.suboptimal2.get_fitness(has_penalty=False), 'Incorrect fitness for dataset 2')

    def test_withPenalty(self):
        self.assertEqual(235, self.optimal1.get_fitness(has_penalty=True), 'Incorrect fitness for dataset 1')
        self.assertLess(235, self.suboptimal1.get_fitness(has_penalty=True), 'Incorrect fitness for dataset 1')

        self.assertEqual(51, self.optimal2.get_fitness(has_penalty=True), 'Incorrect fitness for dataset 2')
        self.assertLess(51, self.suboptimal2.get_fitness(has_penalty=True), 'Incorrect fitness for dataset 2')


if __name__ == '__main__':
    unittest.main()
