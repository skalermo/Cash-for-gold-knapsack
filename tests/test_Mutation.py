import unittest
from GeneticAlgorithm import mutate


class TestMutations(unittest.TestCase):
    def test_mutate(self):
        chromosome = [0, 1, 1, 1, 1, 0, 0, 0]
        new_chromosome = chromosome.copy()
        mutate(new_chromosome)
        self.assertNotEqual(chromosome, new_chromosome)

        chromosome = [1]*10
        mutate(chromosome)
        self.assertFalse(all(chromosome))


if __name__ == '__main__':
    unittest.main()
