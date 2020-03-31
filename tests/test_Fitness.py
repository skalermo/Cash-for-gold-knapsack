import unittest
from GeneticAlgorithm import fitness


class TestFitness(unittest.TestCase):
    def setUp(self):
        self.data = {'capacity': 10, 'weights': [2, 3.14, 1.98, 5.0, 3.0], 'profits': [40, 50, 100, 95, 30]}
        self.optimal = [1, 0, 1, 1, 0]
        self.suboptimal = [1, 1, 1, 1, 1]

    def test_withoutPenalty(self):
        self.assertEqual(235, fitness(self.optimal, self.data, has_penalty=False), 'Incorrect fitness')
        self.assertLess(235, fitness(self.suboptimal, self.data, has_penalty=False), 'Incorrect fitness')

    def test_withPenalty(self):
        self.assertEqual(235, fitness(self.optimal, self.data, has_penalty=True), 'Incorrect fitness')
        self.assertLess(235, fitness(self.suboptimal, self.data, has_penalty=True), 'Incorrect fitness')


if __name__ == '__main__':
    unittest.main()
