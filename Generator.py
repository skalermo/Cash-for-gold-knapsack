import numpy as np
import random


def gen_data(n: int = 10,
             w_cap: int = 10,
             p_cap: int = 10,
             correlation: float = 0.5,
             capacity: float = None,
             capacity_type: str = 'restrictive',
             seed: int = 0
             ) -> dict:
    """
    Generate data according to formulas:
    (W stands for weights, P - for profits, C - for capacity)

    With approximated correlation
        W[i] := (uniformly) random(0..v)
        P[i] := (uniformly) random(0..v)

    capacity_type: restrictive
        C = 2v

    capacity_type: average
        C = 0.5 * sum(W)

    capacity_type: random
        C = n * avg(W) * random(0..1)

    :param n: Number of items
    :param w_cap: Weight max value
    :param p_cap: Profit max value
    :param correlation: Correlation between profits and weights
    :param capacity: Set capacity explicitly
    :param capacity_type: Restrictive, average or random if not set explicitly
    :param seed: Numpy random seed
    :return: Dictionary with generated data
    """

    np.random.seed(seed)

    weights, profits, real_corr_coef = _gen_correlated_uniform_data(n, w_cap, p_cap, correlation)
    weights = weights.tolist()
    profits = profits.tolist()

    if capacity is None:
        capacity = {
            'restrictive': lambda: 2*w_cap,
            'average': lambda: 0.5*sum(weights),
            'random': lambda: round(np.random.rand()*n*sum(weights)/len(weights), 1)
        }.get(capacity_type, 'restrictive')()
    else:
        capacity_type = 'custom'

    data = {
        'weights': weights,
        'profits': profits,
        'capacity': capacity,
        'capacity_type': capacity_type,
        'correlation': correlation,
        'real_correlation': real_corr_coef,
        'seed': seed
    }
    return data


def _gen_correlated_uniform_data(n: int, sx: float, sy: float, corr_coef: float) -> (list, list, float):
    """
    Generate data uniformly from (0,sx)x(0,sy) with set correlation coefficient.
    Based on http://www.acooke.org/random.pdf.
    X and Y are rounded to 1 decimal place
    :param n: Number of samples
    :param sx: X cap
    :param sy: Y cap
    :param corr_coef: Positive correlation between x and y.
    :return: X, Y, real correlation coefficient
    """

    assert 0 <= corr_coef <= 1

    # adjust correlation coefficient
    t = 1 - __adjustment_function(corr_coef)

    # generate points from (0,1)x(0,1), (0,t)x(0,1) and (1-t,1)x(0,1)
    X = np.hstack([np.random.uniform(size=n),
                   np.random.uniform(low=0, high=t, size=round(t * n)),
                   np.random.uniform(low=1-t, high=1, size=round(t * n))])

    Y = np.hstack([np.random.uniform(size=n),
                   np.random.uniform(low=0, high=t, size=round(t * n)),
                   np.random.uniform(low=1-t, high=1, size=round(t * n))])
    points = np.array([X, Y])

    # scale by (sqrt(2), t*sqrt(2))
    scale_matrix = np.array([[np.sqrt(2), 0],
                             [0, t * np.sqrt(2)]])
    points = np.dot(scale_matrix, points)

    # translate by vector (0, -t*sqrt(2)/2)
    points = points - np.array([[0], [t * np.sqrt(2) / 2]])

    # rotate counterclockwise through -45 deg about the origin
    rotate_matrix = np.array([[np.sqrt(2) / 2, -np.sqrt(2) / 2],
                              [np.sqrt(2) / 2, np.sqrt(2) / 2]])
    points = np.dot(rotate_matrix, points)

    # scale by (sx, sy)
    scale_matrix = np.array([[sx, 0],
                             [0, sy]])
    points = np.dot(scale_matrix, points)

    # find points within range (0,1)x(0,1)
    # it's 0.05 because of round operation later
    ids = (0.05 < points[0]) & (points[0] < sx) & (0.05 < points[1]) & (points[1] < sy)
    X = np.round(points[0][ids][:n], 1)
    Y = np.round(points[1][ids][:n], 1)

    # calc real correlation coefficient
    real_corr_coef = np.corrcoef(X, Y)[0, 1]

    return X, Y, real_corr_coef


def __adjustment_function(x):
    """
    Magick function based on Lagrange interpolation.
    Adjusts correlation coefficient.
    """
    return 843.491 * x ** 9 - 3747.36 * x ** 8 + 6991.44 * x ** 7 - \
        7112.28 * x ** 6 + 4290.12 * x ** 5 - 1566.84 * x ** 4 +\
        342.07 * x ** 3 - 43.6857 * x ** 2 + 4.04011 * x
