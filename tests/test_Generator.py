from unittest import TestCase
from datetime import datetime
import numpy as np
from Generator import gen_data, _gen_correlated_uniform_data


class TestGenerator(TestCase):
    def setUp(self) -> None:
        np.random.seed(datetime.now().microsecond)

    def test_gen_data_seed(self):
        # test if data is identical if seed is the same

        random_seed = np.random.randint(0, 1_000_000)
        data1 = gen_data(seed=random_seed)
        data2 = gen_data(seed=random_seed)
        self.assertEqual(data1, data2)

    def test_gen_data_not_none(self):
        # test if data items are not None

        data = gen_data()
        self.assertTrue(all([value is not None for _, value in data.items()]))

    def test_gen_data_list_size(self):
        # test if list size match to provided n argument

        n = np.random.randint(5, 100)
        data = gen_data(n=n)
        self.assertEqual(n, len(data['weights']))
        self.assertEqual(n, len(data['profits']))

    def test_gen_data_in_range(self):
        # test if weights and profits lie withing acceptable range

        w_cap = np.random.randint(50, 150)
        data = gen_data(n=1_000_000, w_cap=w_cap, p_cap=w_cap)
        self.assertTrue(all([(0 < w <= w_cap) & (0 < p <= w_cap) for w, p in zip(data['weights'], data['profits'])]))

    def test_gen_data_strong_corr(self):
        # test if correlation of 1 equals real correlation (up to 3 decimal places)

        n = np.random.randint(100, 200)
        w_cap = np.random.randint(50, 100)
        data = gen_data(n=n, w_cap=w_cap, correlation=1.0)
        self.assertAlmostEqual(1, np.corrcoef(data['weights'], data['profits'])[0, 1], places=3)

    def test_gen_data_explicit_capacity(self):
        # test explicit capacity behavior

        w_cap = 10
        data = gen_data(w_cap=w_cap, capacity=100, capacity_type='restrictive')
        self.assertNotEqual(20, data['capacity'])
        self.assertEqual(100, data['capacity'])
        self.assertEqual('custom', data['capacity_type'])

    def test_gen_data_restrictive_capacity(self):
        # test restrictive capacity behavior

        w_cap = np.random.randint(10, 100)
        data = gen_data(w_cap=w_cap, capacity_type='restrictive')
        self.assertEqual(2*w_cap, data['capacity'])

    def test_gen_data_average_capacity(self):
        # test average capacity behavior

        n = np.random.randint(100, 200)
        data = gen_data(n=n, capacity_type='average')
        self.assertEqual(0.5*sum(data['weights']), data['capacity'])

    def test_gen_data_corr(self):
        # test if correlation error is less than 0.2

        n = np.random.randint(100, 200)
        w_cap = np.random.randint(50, 100)
        correlation = 0.4
        data = gen_data(n=n, w_cap=w_cap, correlation=correlation)
        self.assertTrue(0.2 < np.corrcoef(data['weights'], data['profits'])[0, 1] < 0.6)

    def test_gen_correlated_uniform_data_avg_error(self):
        # test average correlation error

        N = 1000
        tolerated_avg_error = 0.05
        for test_corr_coef in (0.25, 0.5, 0.75):
            error_sum = 0.0
            for _ in range(N):
                np.random.seed(datetime.now().microsecond)
                _, _, coef = _gen_correlated_uniform_data(1000, 100, 100, test_corr_coef)
                error_sum += abs(coef - test_corr_coef)
            # print(error_sum/N)
            self.assertTrue(error_sum/N < tolerated_avg_error)
