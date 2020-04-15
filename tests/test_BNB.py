import unittest
from BNBAlgorithm import knapsack


class BNBTesting(unittest.TestCase):

    def test(self, capacity=None, weights=None, profits=None, optimal=None):
        if not all([capacity, weights, profits, optimal]):
            return

        # Items from weights and profits
        items = [{'weight': w, 'value': p} for (w, p) in zip(weights, profits)]

        # Optimal selection
        result = [items[i] for i in range(len(optimal)) if optimal[i] == 1]

        # Max profit from optimal selection
        max_profit = sum(item['value'] for item in result)

        # Sort Items according to val/weight ratio
        profits, weights = (list(t) for t in zip(*sorted(zip(profits, weights),
                                                         key=lambda tup: tup[0] / tup[1], reverse=True)))

        # Create dict with sorted values
        data = {'capacity': capacity, 'weights': weights, 'profits': profits}

        # Run algorithm
        n = knapsack(data)

        self.assertEqual(max_profit, n.profit, "Wrong profit")
        self.assertTrue(all(x in result for x in n.items), "Wrong selection")

    def test_simple(self):
        capacity = 10
        weights = [ 2, 3.14, 1.98, 5.0, 3.0]
        profits = [40,   50,  100,  95,  30]
        optimal = [ 1,    0,    1,   1,   0]

        self.test(capacity, weights, profits, optimal)

    # Testing data from https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
    def test_P01(self):
        capacity = 165
        weights = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
        profits = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
        optimal = [ 1,  1,  1,  1,  0,  1,  0,  0,  0,  0]

        self.test(capacity, weights, profits, optimal)

    def test_P02(self):
        capacity = 26
        weights = [12,  7, 11,  8,  9]
        profits = [24, 13, 23, 15, 16]
        optimal = [ 0,  1,  1,  1,  0]

        self.test(capacity, weights, profits, optimal)

    def test_P03(self):
        capacity = 190
        weights = [56, 59, 80, 64, 75, 17]
        profits = [50, 50, 64, 46, 50,  5]
        optimal = [ 1,  1,  0,  0,  1,  0]

        self.test(capacity, weights, profits, optimal)

    def test_P04(self):
        capacity = 50
        weights = [31, 10, 20, 19, 4, 3,  6]
        profits = [70, 20, 39, 37, 7, 5, 10]
        optimal = [ 1,  0,  0,  1, 0, 0,  0]

        self.test(capacity, weights, profits, optimal)

    def test_P05(self):
        capacity = 104
        weights = [ 25,  35,  45,  5, 25, 3, 2, 2]
        profits = [350, 400, 450, 20, 70, 8, 5, 5]
        optimal = [  1,   0,   1,  1,  1, 0, 1, 1]

        self.test(capacity, weights, profits, optimal)

    def test_P06(self):
        capacity = 170
        weights = [ 41,  50,  49,  59,  55,  57,  60]
        profits = [442, 525, 511, 593, 546, 564, 617]
        optimal = [  0,   1,   0,   1,   0,   0,   1]

        self.test(capacity, weights, profits, optimal)

    def test_P07(self):
        capacity = 750
        weights = [ 70,  73,  77,  80,  82,  87,  90,  94,  98, 106, 110, 113, 115, 118, 120]
        profits = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]
        optimal = [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]

        self.test(capacity, weights, profits, optimal)

    def test_P08(self):
        capacity = 6404180
        weights = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856,
                   670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]

        profits = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289,
                   1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261]

        optimal = [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1]

        self.test(capacity, weights, profits, optimal)


if __name__ == '__main__':
    unittest.main()
