import random
from datetime import datetime
import numpy as np


class Chromosome:

    def __init__(self, gene):
        self.gene = gene
        self.fitness = 0

    def __setitem__(self, key, value):
        self.gene[key] = value

    def __getitem__(self, key):
        return self.gene[key]

    def copy(self):
        return Chromosome(self.gene.copy())

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

        # Set seed
        if seed is None:
            seed = datetime.now().microsecond
        random.seed(seed)

        # Choose crossover point
        if point is None:
            point = random.randint(0, len(x) - 1)

        # Cross genes
        child1 = x[:point] + y[point:]
        child2 = y[:point] + x[point:]

        return child1, child2

    def mutate(self):
        """
        Select and flip random bit in chromosome
        """

        idx = random.randint(0, len(self.gene) - 1)
        self.gene[idx] = 1 - self.gene[idx]

    def get_fitness(self, data, has_penalty=False):
        if self.fitness <= 0:
            self.fitness = self.calc_fitness(data, has_penalty)

        return self.fitness

    def calc_fitness(self, data, has_penalty):
        """
        Fitness evaluation function with logarithmic penalty function

        :param data:        Dictionary with weights, capacity and profits
        :param has_penalty: Boolean. If True - use penalty function
        :return:            Fitness evaluation
        """

        penalty = 0
        if has_penalty:
            weight_sum = sum([self.gene[i] * data['weights'][i] for i in range(len(self.gene))])
            if weight_sum > data['capacity']:
                # Get p = max(P[i] / W[i])
                p = data['ratios'][0]

                # Find weight_sum = sum(x[i] * W[i]) - C
                weight_sum -= data['capacity']

                # Set penalty
                penalty = np.log2(1 + p * weight_sum)

        # Find fitness = sum(x[i] * P[i] - Penalty(x))
        return sum([self.gene[i] * data['profits'][i] for i in range(len(self.gene))]) - penalty

