
from functools import partial

import matplotlib.pyplot as plt
import numpy as np


def lambda_t(t_upper, productivity, r, t, delta):
    """This function calculates the value of the multiplier at time t.."""
    rslt = 1
    rslt *= ((productivity * np.exp(-r * t)) / (r + delta))
    rslt *= (1.0 - np.exp(-(r + delta) * (t_upper - t)))
    return rslt


def g(x):
    """This function parameterizes the production function of human capital."""
    return x ** 0.71


def g_prime(x):
    """This function parameterizes the marginal effect of studying on the level of human capital."""
    return 0.71 * (x ** (- 0.29))


def crit_func(productivity, r, t, delta, theta, h_t, s_t):

    return (- productivity * np.exp(-r * t) + lambda_t(t_upper, productivity, r, t, delta) *
                theta * g_prime(s_t * h_t)) ** 2

productivity = 0.75
delta = 0.06
r = 0.05
t_upper = 60
theta = 0.5

s_grid = np.linspace(0.01,  1.00, num=500, endpoint=True)
t_grid = np.linspace(0.00, 60.00, num=60, endpoint=True)

s_time = []

for t in t_grid:
    if t == 0.0:
        h_t = 5
    else:
        h_t = (1 - delta) * h_lagged + theta * g(s_t * h_lagged)



    crit_func = partial(crit_func, productivity, r, t, delta, theta)
    crit_func = np.vectorize(crit_func)

    s_t = s_grid[np.argmin(crit_func(h_t, s_grid))]

    h_lagged = h_t

    s_time += [s_t]


fig, ax = plt.subplots()
ax.plot(t_grid, s_time)


plt.savefig('test.png')