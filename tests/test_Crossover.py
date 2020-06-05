import unittest
from Chromosome import Chromosome


class TestCrossover(unittest.TestCase):

    def test_randSinglePoint(self):
        parents = (Chromosome([1, 1, 1, 1, 1, 1]), Chromosome([0, 0, 0, 0, 0, 0]))
        results = (Chromosome([1, 1, 1, 1, 0, 0]), Chromosome([0, 0, 0, 0, 1, 1]))

        children = Chromosome.crossover(parents, seed=5)

        self.assertEqual(len(parents[0]), len(children[0]), "Children are not same length")
        self.assertEqual(len(parents[1]), len(children[1]), "Children are not same length")
        self.assertEqual(results, children, "Incorrect result")

    def test_constSinglePoint(self):
        parents = (Chromosome([1, 1, 1, 1, 1, 1]), Chromosome([0, 0, 0, 0, 0, 0]))
        results = (Chromosome([1, 1, 1, 0, 0, 0]), Chromosome([0, 0, 0, 1, 1, 1]))

        children = Chromosome.crossover(parents, point=3)

        self.assertEqual(len(parents[0]), len(children[0]), "Children are not same length")
        self.assertEqual(len(parents[1]), len(children[1]), "Children are not same length")
        self.assertEqual(results, children, "Incorrect result")


if __name__ == '__main__':
    unittest.main()
