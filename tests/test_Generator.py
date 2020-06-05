from unittest import TestCase
import random
from datetime import datetime
from numpy import corrcoef
from Generator import gen_data


class TestGenerator(TestCase):
    def setUp(self) -> None:
        random.seed(datetime.now().microsecond)

    def test_gen_data_seed(self):
        random_seed = random.randint(0, 1_000_000)
        data1 = gen_data(seed=random_seed)
        data2 = gen_data(seed=random_seed)
        self.assertEqual(data1, data2)

    def test_machine_independent_seed(self):
        data = {'n': 5,
                'weights': [6.8, 1.2, 3.5, 3.0, 7.6],
                'profits': [8.6, 5.1, 2.7, 0.20000000000000018, 7.699999999999999],
                'ratios': [1.2647058823529411, 4.25, 0.7714285714285715, 0.06666666666666672, 1.013157894736842],
                'sorted_indices': [1, 0, 4, 2, 3], 'capacity': 20, 'capacity_type': 'restrictive', 'correlation': 'weak',
                'seed': 42}
        self.assertEqual(data, gen_data(n=5, seed=42))

    def test_gen_data_not_none(self):
        data = gen_data()
        self.assertTrue(all([value is not None for _, value in data.items()]))

    def test_gen_data_list_size(self):
        n = random.randint(5, 100)
        data = gen_data(n=n)
        self.assertEqual(n, len(data['weights']))
        self.assertEqual(n, len(data['profits']))

    def test_gen_data_negative_profits(self):
        data = gen_data(n=1_000_000)
        self.assertTrue(all([x > 0.0 for x in data['profits']]))

    def test_gen_data_in_range(self):
        v = random.randint(50, 150)
        data = gen_data(n=100, v=v)
        self.assertTrue(all([1 <= x <= v for x in data['weights']]))

    def test_gen_data_strong_corr(self):
        n = random.randint(100, 200)
        r = random.randint(20, 60)
        data = gen_data(n=n, r=r, correlation='strong')
        self.assertEqual('strong', data['correlation'])
        self.assertAlmostEqual(1, corrcoef(data['weights'], data['profits'])[0, 1])

    def test_gen_data_weak_corr(self):
        n = random.randint(100, 200)
        v = random.randint(100, 150)
        r = random.randint(20, 60)
        data = gen_data(n=n, v=v, r=r, correlation='weak')
        self.assertTrue(0.2 < corrcoef(data['weights'], data['profits'])[0, 1] < 1)

    def test_gen_data_explicit_capacity(self):
        v = 10
        data = gen_data(v=v, capacity=100, capacity_type='restrictive')
        self.assertNotEqual(20, data['capacity'])
        self.assertEqual(100, data['capacity'])

    def test_gen_data_restrictive_capacity(self):
        v = random.randint(1, 100)
        data = gen_data(v=v, capacity_type='restrictive')
        self.assertEqual(2*v, data['capacity'])

    def test_gen_data_average_capacity(self):
        n = random.randint(100, 200)
        data = gen_data(n=n, capacity_type='average')
        self.assertEqual(0.5*sum(data['weights']), data['capacity'])

    def test_gen_data_field_n(self):
        n = random.randint(100, 200)
        data = gen_data(n=n)
        self.assertEqual(n, data['n'])

    def test_gen_data_field_ratio(self):
        data = gen_data()
        for i in range(data['n']):
            self.assertEqual(data['ratios'][i], data['profits'][i]/data['weights'][i])

    def test_gen_data_if_sorted(self):
        data = gen_data()
        self.assertTrue(all(data['ratios'][i] >= data['ratios'][j] for i, j in
                            zip(data['sorted_indices'][:-2], data['sorted_indices'][:-1])))
