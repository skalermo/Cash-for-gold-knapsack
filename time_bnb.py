from BNBAlgorithm import knapsack
from Generator import gen_data
from time import time
from GeneticAlgorithm import init_population, next_generation, genetic_algorithm
from DrawUnit import DrawUnit


def timeit(fun, *args):
    start = time()
    fun(*args)
    passed = time() - start
    return passed


def main():
    draw_unit = DrawUnit()
    times = []
    elements = []
    instances = 5
    # data = gen_data(40, capacity_type='average')
    # s, p, b = knapsack(data)
    # print(s.profit)
    # p_max = max(p)

    data = gen_data(100, capacity_type='restrictive')

    populations = [init_population(100, data)]

    draw_unit.add_pop_to_plot(populations[-1], len(populations)-1)

    for i in range(5):
        for _ in range(10):
            populations.append(next_generation(data, populations[-1],
                                               crossover_rate=1, mutation_rate=0.5))

        draw_unit.add_pop_to_plot(populations[-1], len(populations) - 1)

    print(populations[-1][0].gene)

    draw_unit.show()

    # plt.plot(p)
    # plt.plot(b)
    # plt.show()

    # try:
    #     for i in range(10, 501, 5):
    #         sum = 0
    #         for _ in range(instances):
    #             data = gen_data(i, capacity_type='average')
    #             sum += timeit(knapsack, data)
    #         times.append(sum/instances)
    #         elements.append(i)
    #         print(i, sum/instances)
    # except KeyboardInterrupt:
    #     pass

    # plt.plot(elements, times)
    # plt.ylabel('Seconds')
    # plt.xlabel('Elements in knapsack')
    # plt.show()


if __name__ == '__main__':
    main()
