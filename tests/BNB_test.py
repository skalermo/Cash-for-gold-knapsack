import unittest
from BNBAlgorithm import knapsack, Item


class BNBTesting(unittest.TestCase):

    def test(self, capacity=None, weights=None, profits=None, optimal=None):
        if not all([capacity, weights, profits, optimal]):
            return

        items = [Item(w, p) for (w, p) in zip(weights, profits)]
        result = [items[i] for i in range(len(optimal)) if optimal[i] == 1]
        max_profit = sum(i.value for i in result)

        n = knapsack(capacity, items, len(items))

        self.assertEqual(max_profit, n.profit, "Wrong profit")
        self.assertTrue(all(x in result for x in n.items), "Wrong selection")

    def test_one(self):
        W = 10
        weights = [ 2, 3.14, 1.98, 5.0, 3.0]
        profits = [40,   50,  100,  95,  30]
        optimal = [ 1,    0,    1,   1,   0]

        self.test(W, weights, profits, optimal)

    def test_two(self):
        W = 165
        weights = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
        profits = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
        optimal = [ 1,  1,  1,  1,  0,  1,  0,  0,  0,  0]

        self.test(W, weights, profits, optimal)


if __name__ == '__main__':
    unittest.main()
