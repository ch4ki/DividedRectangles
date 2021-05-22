from utility import *


class Interval:
    def __init__(self, c, y, depths):
        self.c = c
        self.y = y
        self.depths = depths


def min_depth(interval):
    mini = np.min(interval.depths)
    return mini


def reparameterize_to_unit_hypercube(fun, a, b):
    delta = np.subtract(b, a)
    return lambda x: fun(np.multiply(x, delta) + b)


def rev_unit_hypercube_parameterization(x, a, b):
    return np.multiply(x, b - a) + a


def add_interval(intervals, interval):
    d = int(min_depth(interval))
    if d in intervals:
        pass
    else:
        intervals[d] = PriorityQueue()
    return intervals[d].put((interval, interval.y))


Intervals = {}


def divide(f, interval):
    c, d, n = np.array(interval.c), min_depth(interval), len(interval.c)
    dirs = np.asarray(np.where(interval.depths == d))[0]

    cs = [(c + np.multiply(3.0 ** (-d - 1), basis(i, n)), c - np.multiply((3.0 ** (-d - 1)), basis(i, n))) for i in
          dirs]
    vs = [(f(C[0]), f(C[1])) for C in cs]

    minvals = [np.min(V) for V in vs]
    intervals = []
    depths = np.copy(interval.depths)
    for j in np.argsort(minvals):
        # print(dirs[j])
        # print(depths[dirs[j]])
        depths[dirs[j]] += 1
        C, V = cs[j], vs[j]
        intervals.append(Interval(C[0], V[0], np.copy(depths)))
        intervals.append(Interval(C[1], V[1], np.copy(depths)))
    intervals.append(Interval(c, interval.y, np.copy(depths)))
    return intervals


def slope(y, y1, x, x1):
    if x == x1:
        x1 = x1 + 1E-8
    return (y - y1) / (x - x1)


def get_opt_intervals(intervals, eps, y_best):
    max_depth = np.max(list(intervals.keys()))

    stack = [peek(intervals[max_depth])[0]]
    d = max_depth
    while d >= 0:

        if d in intervals and len(intervals[d]) != 0:
            interval = peek(intervals[d])[0]
            x, y = 0.5 * 3.0 ** (-min_depth(interval)), interval.y
            while len(stack) != 0:
                interval1 = stack[-1]
                x1 = 0.5 * 3.0 ** (-min_depth(interval1))
                y1 = interval1.y

                l1 = slope(y, y1, x, x1)
                # if (l1 == nan)
                if y1 - l1 * x1 > y_best - eps or y < y1:
                    stack.pop()
                elif len(stack) > 1:
                    interval2 = stack[-2]
                    x2 = 0.5 * 3.0 ** (-min_depth(interval2))
                    y2 = interval2.y
                    l2 = (y1 - y2) / (x1 - x2)
                    if l2 > l1:
                        stack.pop()
                    else:
                        break
                else:
                    break
            stack.append(interval)
        d = d - 1
    return stack


def direct(fun, a, b, eps, k_max):
    g = reparameterize_to_unit_hypercube(fun, a, b)
    intervals = Intervals
    n = len(a)
    c = np.empty(n)
    c.fill(0.5)
    filling = np.empty(n)
    filling.fill(0)
    interval = Interval(c, g(c), filling)

    add_interval(intervals, interval)

    c_best, y_best = np.copy(interval.c), interval.y
    for k in range(k_max):
        S = get_opt_intervals(intervals, eps, y_best)
        to_add = []
        for interval in S:
            to_add.append(divide(g, interval))

            del intervals[min_depth(interval)]

        for interval in to_add[0]:
            add_interval(intervals, interval)
            if interval.y < y_best:
                c_best, y_best = np.copy(interval.c), interval.y

    return rev_unit_hypercube_parameterization(c_best, a, b)
