from contextlib import contextmanager

from matplotlib import pyplot as plot
from matplotlib import style
from functools import wraps
from pylab import rcParams

import numpy as np
import time


rcParams['figure.figsize'] = 20, 30
style.use('fivethirtyeight')


@contextmanager
def plotting(**outer):
    fig = plot.figure()
    i = 0

    def draw(fn, cmp=None, **inner):
        inner = {
            'cmp': cmp,
            **outer,
            **inner
        }

        data_fn = inner.pop('data_fn')
        cmp = inner.pop('cmp')
        start = inner.pop('start', 10)
        stop = inner.pop('stop', 1000)
        step = inner.pop('step', 1)
        N = inner.pop('N', 100)
        desc = inner.pop('desc', '')
        ylim = inner.pop('ylim', None)


        space = range(start, stop, step)
        timed_fn = timer(fn)

        dataset = [[data_fn(n) for _ in range(N)] for n in space]
        results = [timed_fn(data) for data in dataset]

        nonlocal i
        i += 1

        sp = fig.add_subplot(2, 1, i)
        sp.plot(space, results)

        if cmp:
            x = np.array(space)
            y = np.array(space)

            sp.plot(x, cmp(y) * compl_n)

        sp.set_title(desc)
        if ylim:
            sp.set_ylim(ylim)

    yield draw
    plot.show()


def timer(fn):
    @wraps(fn)
    def wrapper(dataset):
        print('Testing {} with n = {}'.format(fn, len(dataset[0])))
        t = time.clock()
        for data in dataset:
            fn(data)

        return (time.clock() - t) / len(dataset)

    return wrapper


def linear_time(n):
    @timer
    def n_test(xs):
        acc = 1
        for x in xs:
            acc *= x + 0.1

        return acc

    xs = [list(range(n)) for _ in range(1000)]
    time = n_test(xs)
    return time

compl_n = linear_time(1000) / 1000
