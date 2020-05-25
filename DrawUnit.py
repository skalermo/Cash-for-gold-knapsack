import matplotlib.pyplot as plt


class DrawUnit:
    def __init__(self, mode='roulette', data=None):
        self.data = data
        self.mode = mode

        ax = plt.axes()
        ax.yaxis.set_major_locator(plt.NullLocator())
        ax.xaxis.set_major_locator(plt.NullLocator())
        plt.xlabel('Low bits weighted sum', fontsize=12)
        plt.ylabel('High bits weighted sum', fontsize=12)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.gca().set_aspect('equal', adjustable='box')

    def show(self):
        plt.legend(loc='best')
        plt.show()

    def add_pop_to_plot(self, pop, no):
        plt.plot(*zip(*self.population_to_coords(pop)),
                 marker='o', ls='', label=f'pop {no}')

    def population_to_coords(self, pop):
        result = []
        for p in pop:
            result.append(self.bitarray_to_coords(p))
        return result

    def bitarray_to_coords(self, a):
        high = a[:len(a) // 2]
        low = a[len(a) // 2:]
        x, y = 0, 0
        for i in range(len(high)):
            y += high[i] * self.calc_weight(i, len(high))
        for i in range(len(low)):
            x += low[i] * self.calc_weight(i, len(low))
        return [x, y]

    def calc_weight(self, i, n):
        mode = self.mode
        if self.mode == 'data' and self.data is None:
            mode = 'roulette'

        if mode == 'equal':
            return 1/n
        if mode == 'pow_of_2':
            return 1/2**(i+1)
        if mode == 'roulette':
            return 2*(n-i)/(n*(n+1))
        if mode == 'data':
            return self.data['ratios'][i]/sum(self.data['ratios'])
        return 0
