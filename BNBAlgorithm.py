from queue import Queue


class Item:
    def __init__(self, w: float, v: int):
        self.weight = w
        self.value = v

    def __str__(self):
        return '({0}, {1})'.format(self.weight, self.value)


class Node:
    def __init__(self, l, p, w, b):
        self.level = l
        self.profit = p
        self.bound = b
        self.weight = w

    def copy(self):
        return Node(self.level, self.profit, self.weight, self.bound)

    def __str__(self):
        return '{}|{}|{}|{}'.format(self.level, self.profit, self.weight, self.bound)


def bound(u: Node, n, W, arr):
    if u.weight >= W:
        return 0

    profit_bound = u.profit

    j = u.level + 1
    tot_weight = u.weight

    while (j < n) and (tot_weight + arr[j].weight <= W):
        tot_weight += arr[j].weight
        profit_bound += arr[j].value
        j += 1

    if j < n:
        profit_bound += (W - tot_weight) * arr[j].value // arr[j].weight

    return profit_bound


def knapsack(W, arr, n):
    arr.sort(key=lambda x: x.value / x.weight, reverse=True)

    Q = Queue()

    u = Node(l=-1, p=0, w=0.0, b=0)
    v = Node(None, None, None, None)
    Q.put((u, -1))

    max_profit = 0
    while not Q.empty():
        u, node = Q.get()
        print(u, node)

        if u.level == -1:
           v.level = 0

        if u.level == n - 1:
            continue

        v.level = u.level + 1

        v.weight = u.weight + arr[v.level].weight
        v.profit = u.profit + arr[v.level].value

        if v.weight <= W and v.profit > max_profit:
            max_profit = v.profit

        v.bound = bound(v, n, W, arr)

        if v.bound > max_profit:
            Q.put((v.copy(), arr[v.level]))

        v.weight = u.weight
        v.profit = u.profit
        v.bound = bound(v, n, W, arr)
        if v.bound > max_profit:
            Q.put((v.copy(), arr[v.level]))

    return max_profit


W = 10

arr = [Item(2.0, 40), Item(3.14, 50), Item(1.98, 100), Item(5.0, 95), Item(3.0, 30)]

n = 5

print(knapsack(W, arr, n))



