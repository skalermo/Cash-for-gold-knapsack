import unittest
from GeneticAlgorithm import mutate


class TestMutations(unittest.TestCase):
    def test_mutate(self):
        chromosome = [0, 1, 1, 1, 1, 0, 0, 0]
        chromosome_mutated = chromosome.copy()
        mutate(chromosome_mutated)
        self.assertNotEqual(chromosome, chromosome_mutated)

        chromosome = [1]*10
        chromosome_mutated = chromosome.copy()
        mutate(chromosome_mutated)
        self.assertFalse(all(chromosome_mutated))

        chromosome = [0]*10
        chromosome_mutated = chromosome.copy()
        mutate(chromosome_mutated)
        self.assertTrue(any(chromosome_mutated))


if __name__ == '__main__':
    unittest.main()
