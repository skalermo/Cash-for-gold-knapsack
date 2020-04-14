import unittest
from GeneticAlgorithm import fitness


class TestFitness(unittest.TestCase):
    def setUp(self):
        self.data1 = {'capacity': 10, 'weights': [2, 3.14, 1.98, 5.0, 3.0], 'profits': [40, 50, 100, 95, 30]}
        self.optimal1 = [1, 0, 1, 1, 0]

        self.data2 = {'capacity': 26, 'weights': [12,  7, 11,  8,  9], 'profits': [24, 13, 23, 15, 16]}
        self.optimal2 = [0, 1, 1, 1, 0]

        self.suboptimal = [1, 1, 1, 1, 1]

    def test_withoutPenalty(self):
        self.assertEqual(235, fitness(self.optimal1, self.data1, has_penalty=False), 'Incorrect fitness for dataset 1')
        self.assertLess(235, fitness(self.suboptimal, self.data1, has_penalty=False), 'Incorrect fitness for dataset 1')

        self.assertEqual(51, fitness(self.optimal2, self.data2, has_penalty=False), 'Incorrect fitness for dataset 2')
        self.assertLess(51, fitness(self.suboptimal, self.data2, has_penalty=False), 'Incorrect fitness for dataset 2')

    def test_withPenalty(self):
        self.assertEqual(235, fitness(self.optimal1, self.data1, has_penalty=True), 'Incorrect fitness for dataset 1')
        self.assertLess(235, fitness(self.suboptimal, self.data1, has_penalty=True), 'Incorrect fitness for dataset 1')

        self.assertEqual(51, fitness(self.optimal2, self.data2, has_penalty=True), 'Incorrect fitness for dataset 2')
        self.assertLess(51, fitness(self.suboptimal, self.data2, has_penalty=True), 'Incorrect fitness for dataset 2')


if __name__ == '__main__':
    unittest.main()
