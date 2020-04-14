import unittest
from Generator import gen_data
from GeneticAlgorithm import init_population, selection


class TestSelection(unittest.TestCase):
    def test_selection_output_size(self):
        data = gen_data()
        population = init_population(50, data)
        selected = selection(population, 0, 50)
        self.assertEqual(50, len(selected))


if __name__ == '__main__':
    unittest.main()
