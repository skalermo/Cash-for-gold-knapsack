import unittest
from GeneticAlgorithm import mutate


class TestMutations(unittest.TestCase):
    def test_mutate(self):
        chromosome = [0, 1, 1, 1, 1, 0, 0, 0]
        mutated = mutate(chromosome)
        self.assertNotEqual(chromosome, mutated)

        chromosome = [1]*10
        mutated = mutate(chromosome)
        self.assertFalse(all(mutated))

        chromosome = [0]*10
        mutated = mutate(chromosome)
        self.assertTrue(any(mutated))


if __name__ == '__main__':
    unittest.main()
