import random
from datetime import datetime
import numpy as np
import itertools


class Chromosome:

    def __init__(self, gene, data=None):
        # always set data, unless running in tests

        self.gene = gene
        self.fitness = float('-inf')
        self.data = data
        if data:
            self.weight_sum = sum(itertools.compress(data['weights'], self.gene))

    def __setitem__(self, key, value):
        self.gene[key] = value

    def __getitem__(self, key):
        return self.gene[key]

    def __len__(self):
        return len(self.gene)

    def __eq__(self, other):
        return self.gene == other.gene

    def repair(self, mode='greedy'):
        """
        Repair chromosome by removing extra elements.
        Inplace operation.
        There are two modes: greedy and random.
        """
        assert mode in ['greedy', 'random']
        i = idx = 0

        while self.is_overfilled():
            i -= 1
            if mode == 'random':
                idx = i
            if mode == 'greedy':
                idx = self.data['sorted_indices'][i]

            self.weight_sum -= self.data['weights'][idx] * self.gene[idx]
            self.gene[idx] = 0

    def copy(self):
        return Chromosome(self.gene.copy(), self.data)

    @staticmethod
    def crossover(parents, seed=None, point=None):
        """
        Single point crossover.
        Produce two offsprings, each carrying some genetic information from both parents.

        (If point is set, seed has no effect on choosing crossover point)

        :param parents: Chromosome pair
        :param seed:    Random seed
        :param point:   Crossover point
        :return:        2 children
        """
        x, y = parents
        data = None
        if x.data:
            data = x.data
        x, y = x.gene, y.gene

        # Set seed
        if seed is None:
            seed = datetime.now().microsecond
        random.seed(seed)

        # Choose crossover point
        if point is None:
            point = random.randint(0, len(x) - 1)

        # Cross genes
        # child1 = x[:point] + y[point:]
        # child2 = y[:point] + x[point:]

        # Alternative crossover: choose random bits and swap 'em
        child1 = x[:]
        child2 = y[:]
        k = random.randint(1, data['n']//2)
        genes_to_swap = random.sample(range(data['n']), k)
        for i in genes_to_swap:
            child1[i], child2[i] = child2[i], child1[i]

        return Chromosome(child1, data), Chromosome(child2, data)

    def mutate(self):
        """
        Select and flip random bit in chromosome
        """

        idx = random.randint(0, len(self.gene) - 1)
        self.weight_sum -= self.data['weights'][idx] * self.gene[idx]
        self.gene[idx] = 1 - self.gene[idx]
        self.weight_sum += self.data['weights'][idx] * self.gene[idx]

    def get_fitness(self, has_penalty=True):
        if self.fitness <= 0:
            self.fitness = self.calc_fitness(has_penalty)

        return self.fitness

    def calc_fitness(self, has_penalty):
        """
        Fitness evaluation function with logarithmic penalty function

        :param data:        Dictionary with weights, capacity and profits
        :param has_penalty: Boolean. If True - use penalty function
        :return:            Fitness evaluation
        """

        penalty = 0
        if has_penalty:
            if self.weight_sum > self.data['capacity']:
                # Get p = max(P[i] / W[i])
                p = self.data['ratios'][self.data['sorted_indices'][0]]

                # Find sum_diff = sum(x[i] * W[i]) - C
                sum_diff = self.weight_sum - self.data['capacity']

                # Set penalty
                penalty = np.log2(1 + p * sum_diff)
                # penalty = (p * sum_diff)**2

        # Find fitness = sum(x[i] * P[i] - Penalty(x))
        self.fitness = sum(itertools.compress(self.data['profits'], self.gene)) - penalty
        return self.fitness

    def is_overfilled(self):
        return self.weight_sum > self.data['capacity']

    def decode(self):
        return [(profit, weight) for profit, weight in
                zip(list(itertools.compress(self.data['profits'], self.gene)),
                    list(itertools.compress(self.data['weights'], self.gene)))]
