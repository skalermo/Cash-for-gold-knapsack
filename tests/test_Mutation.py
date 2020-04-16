import unittest
from Chromosome import Chromosome


class TestMutations(unittest.TestCase):
    def test_mutate(self):
        chromosome = Chromosome([0, 1, 1, 1, 1, 0, 0, 0])
        chromosome_mutated = chromosome.copy()
        chromosome_mutated.mutate()
        self.assertNotEqual(chromosome.gene, chromosome_mutated.gene)

        chromosome = Chromosome([1]*10)
        chromosome_mutated = chromosome.copy()
        chromosome_mutated.mutate()

        self.assertFalse(all(chromosome_mutated))

        chromosome = Chromosome([0]*10)
        chromosome_mutated = chromosome.copy()
        chromosome_mutated.mutate()
        self.assertTrue(any(chromosome_mutated))


if __name__ == '__main__':
    unittest.main()
