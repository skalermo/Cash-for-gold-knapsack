from queue import Queue


class Item:
    def __init__(self, w: float, v: int):
        self.weight = w
        self.value = v

    def __str__(self):
        return '({0}, {1})'.format(self.weight, self.value)


class Node:
    def __init__(self, l, p, w, b, i=[]):
        self.level = l
        self.profit = p
        self.bound = b
        self.weight = w
        self.items = i

    def copy(self):
        return Node(self.level, self.profit, self.weight, self.bound, self.items.copy())

    def __str__(self):
        s = '{}|{}|{}|{}\n['.format(self.level, self.profit, self.weight,
                                    self.bound, self.items)
        for i in self.items:
            s += str(i) + " "

        return s + "]"


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
    v = u.copy()
    Q.put(u)

    max_node = Node(l=-1, p=0, w=0.0, b=0)
    while not Q.empty():
        u = Q.get()

        if u.level == -1:
            v.level = 0

        if u.level == n - 1:
            continue

        v.level = u.level + 1

        v.weight = u.weight + arr[v.level].weight
        v.profit = u.profit + arr[v.level].value
        v.items = u.items.copy()
        v.items.append(arr[v.level])

        if v.weight <= W and v.profit > max_node.profit:
            max_node = v.copy()

        v.bound = bound(v, n, W, arr)

        if v.bound > max_node.profit:
            Q.put(v.copy())

        v.weight = u.weight
        v.profit = u.profit
        v.items = u.items.copy()

        v.bound = bound(v, n, W, arr)

        if v.bound > max_node.profit:
            Q.put(v.copy())

    return max_node
