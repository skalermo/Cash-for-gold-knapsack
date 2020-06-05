from queue import Queue


# Item class for weight and value
class Item:
    def __init__(self, w: float, v: int):
        self.weight = w
        self.value = v

    def __str__(self):
        return '({0}, {1})'.format(self.weight, self.value)


# Node class for BNB algorithm
class Node:
    def __init__(self, l, p, w, b, i=None):
        if i is None:
            i = []
        self.level = l      # Level of node in decision tree
        self.profit = p     # Profit of nodes on path from root to this node
        self.bound = b      # Upper bound of maximum profit in subtree
        self.weight = w     # Weight sum of nodes
        self.items = i      # Selected items

    def copy(self):
        return Node(self.level, self.profit, self.weight, self.bound, self.items.copy())

    def __str__(self):
        s = '{}|{}|{}|{}\n['.format(self.level, self.profit, self.weight,
                                    self.bound, self.items)
        for i in self.items:
            s += str(i) + " "

        return s + "]"


# Return upper bound of profit in subtree
def bound(u: Node, n, W, arr):
    if u.weight >= W:
        return 0

    # Init profit_bound
    profit_bound = u.profit

    # Start from current index + 1
    j = u.level + 1
    tot_weight = u.weight

    # Check index and knapsack capacity conditions
    while (j < n) and (tot_weight + arr[j].weight <= W):
        tot_weight += arr[j].weight
        profit_bound += arr[j].value
        j += 1

    # Include last item partially for upper bound on profit
    if j < n:
        profit_bound += (W - tot_weight) * arr[j].value // arr[j].weight

    return profit_bound


# Returns best node with maximum profit
def knapsack(data, depth=None):
    capacity = data['capacity']
    items = [Item(w, p) for (w, p) in zip(data['weights'], data['profits'])]
    n = len(items)

    # Sort Items according to val/weight ratio
    items_sorted = sorted(items, key=lambda x: x.value / x.weight, reverse=True)

    # Init queue for nodes
    Q = Queue()

    # Create dummy node and put it in queue
    u = Node(l=-1, p=0, w=0.0, b=0)
    Q.put(u)

    v = Node(None, Node, None, None)

    max_node = Node(l=-1, p=0, w=0.0, b=0)
    while not Q.empty():
        u = Q.get()     # Get node

        if u.level == -1:       # If starting node assign level 0
            v.level = 0

        if u.level == n - 1:    # If there is nothing on next level
            continue

        v.level = u.level + 1   # Increment node level

        # Add current weight and value to u node
        v.weight = u.weight + items_sorted[v.level].weight
        v.profit = u.profit + items_sorted[v.level].value

        # Save added items
        v.items = u.items.copy()
        v.items.append(items_sorted[v.level])

        # If conditions are ok, update max_node
        if v.weight <= capacity and v.profit > max_node.profit:
            max_node = v.copy()

        # Get upper bound to decide if add v to Queue or not
        v.bound = bound(v, n, capacity, items_sorted)

        if v.bound > max_node.profit:
            if depth is None or depth > v.level:
                Q.put(v.copy())

        # Repeat without taking item to knapsack
        v.weight = u.weight
        v.profit = u.profit
        v.items = u.items.copy()

        v.bound = bound(v, n, capacity, items_sorted)

        if v.bound > max_node.profit:
            if depth is None or depth > v.level:
                Q.put(v.copy())

    result = {'profits': max_node.profit, 'optimal': [1 if x in max_node.items else 0 for x in items],
              'depth': max_node.level}
    return result
