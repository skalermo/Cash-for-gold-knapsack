import unittest
from Chromosome import Chromosome
from Generator import gen_data


class TestMutations(unittest.TestCase):
    def setUp(self) -> None:
        self.data = gen_data()

    def test_mutate(self):
        chromosome = Chromosome([0, 1, 1, 1, 1, 0, 0, 0], self.data)
        chromosome_mutated = chromosome.copy()
        chromosome_mutated.mutate()
        self.assertNotEqual(chromosome.gene, chromosome_mutated.gene)

        chromosome = Chromosome([1]*10, self.data)
        chromosome_mutated = chromosome.copy()
        chromosome_mutated.mutate()

        self.assertFalse(all(chromosome_mutated.gene))

        chromosome = Chromosome([0]*10, self.data)
        chromosome_mutated = chromosome.copy()
        chromosome_mutated.mutate()
        self.assertTrue(any(chromosome_mutated.gene))


if __name__ == '__main__':
    unittest.main()
