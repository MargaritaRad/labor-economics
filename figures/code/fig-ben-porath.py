
from functools import partial

import matplotlib.pyplot as plt
import numpy as np


def lambda_t(t_upper, productivity, r, t, delta):
    """This function calculates the value of the multiplier at time t.."""
    rslt = 1
    rslt *= ((productivity * np.exp(-r * t)) / (r + delta))
    rslt *= (1.0 - np.exp(-(r + delta) * (t_upper - t)))
    return rslt


def g(h_t, s_t):
    """This function parameterizes the production function of human capital."""
    return (h_t * s_t) ** 0.71


def g_prime(h_t, s_t):
    """This function parameterizes the marginal effect of studying on the level of human capital."""
    return 0.71 * ((h_t * s_t) ** (- 0.29))


def get_income(productivity, s, h):
    """This function returns the level of income."""
    return productivity * (1 - s) * h


def crit_func(productivity, r, delta, theta, t, t_upper, h_t, s_t):
    """This function solves the first-order condition."""
    rslt = 1
    rslt *= - productivity * np.exp(-r * t)
    rslt += lambda_t(t_upper, productivity, r, t, delta) * theta * g_prime(s_t, h_t)
    return rslt ** 2


def distribute_model(model_dct):
    """Distribute model information."""
    labels = ['productivity', 'delta', 'r', 't_upper', 'theta']
    for label in labels:
        yield model_dct[label]


def simulate_model(model_dct):
    """This function simulates the model for a number of periods."""

    productivity, delta, r, t_upper, theta = distribute_model(model_dct)

    rslt = dict()
    rslt['s_time'] = []
    rslt['w_time'] = []
    rslt['h_time'] = []
    rslt['t_time'] = []

    s_grid = np.linspace(0.01,  1.00, num=500, endpoint=True)
    t_grid = np.linspace(0.00, 60.00, num=60, endpoint=True)

    for t in t_grid:
        if t == 0.0:
            h_current = 5
        else:
            h_current = (1 - delta) * h_lagged + theta * g(s_t, h_lagged)

        func = np.vectorize(partial(crit_func, productivity, r, delta, theta, t, t_upper,
            h_current))
        s_t = s_grid[np.argmin(func(s_grid))]

        # Wage received
        w_t = get_income(productivity, s_t, h_current)
        h_lagged = h_current

        rslt['h_time'] += [h_current]
        rslt['s_time'] += [s_t]
        rslt['w_time'] += [w_t]
        rslt['t_time'] += [t]

    return rslt


from numpy import exp,arange

from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show
# the function that I'm going to plot
def z_func(x,y):
 return (1-(x**2+y**3))*exp(-(x**2+y**2)/2)
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt



h_grid = np.linspace(0.0, 150)
get_income_mod = np.vectorize(partial(get_income, 0.5, 0.5))
i_grid_1 = get_income_mod(h_grid)


h_grid = np.linspace(0.0, 150)
get_income_mod = np.vectorize(partial(get_income, 0.4, 0.5))
i_grid_2 = get_income_mod(h_grid)

ax = plt.figure().add_subplot(111)
plt.xlim(0, 150)
plt.ylim(0, 50)
plt.xlabel(r'$h(t)$')
plt.ylabel(r'Income')

ax.plot(h_grid, i_grid_1, label=r'$A = 0.5$')
ax.plot(h_grid, i_grid_2, label=r'$A = 0.4$')
ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.legend()

plt.savefig('fig-ben-porath-income.png')


# We want to study the production of human capital in more detail and inspect the parametrized
# production function.
ax = plt.figure().add_subplot(111)


x = arange(0.0,1.0,0.1)
y = arange(0.0,150,0.1)
X, Y = meshgrid(x, y) # grid of point

Z = g(X, Y) # evaluation of the function on the grid

im = ax.imshow(Z,cmap=cm.RdBu, aspect='auto', origin='lower', extent=[0, 1, 0, 150]) # drawing the
ax.yaxis.get_major_ticks()[0].set_visible(False)

# function
# adding the Contour lines with labels
cset = contour(Z,arange(0,30, 5),linewidths=2,extent=[0, 1, 0, 150])
clabel(cset,inline=True,fmt='%1.1f')
colorbar(im)
plt.savefig('fig-ben-porath-production-intensity.png')


fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.RdBu,linewidth=0, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig('fig-ben-porath-production-surface.png')


model_dct = dict()
model_dct['productivity'] = 0.75
model_dct['delta'] = 0.06
model_dct['t_upper'] = 60
model_dct['theta'] = 0.5
model_dct['r'] = 0.05

rslt_1 = simulate_model(model_dct)
model_dct['theta'] = 0.4
rslt_2 = simulate_model(model_dct)

t_time = rslt_1['t_time']

# Plot for the share of human capital investment over time.
ax = plt.figure().add_subplot(111)
plt.xlim(0, 60)
plt.ylim(0, 1.01)
plt.xlabel(r'$t$')
plt.ylabel(r'Investment')

ax.plot(t_time, rslt_1['s_time'], label=r'$A = 0.5$')
ax.plot(t_time, rslt_2['s_time'], label=r'$A = 0.4$')
ax.yaxis.get_major_ticks()[0].set_visible(False)
ax.legend()

plt.savefig('fig-ben-porath-life-cycle-investment.png')

ax = plt.figure().add_subplot(111)
plt.xlim(0, 60)
plt.ylim(0, 120.01)
plt.xlabel(r'$t$')
plt.ylabel(r'Human Capital')

ax.plot(t_time, rslt_1['h_time'], label=r'$A = 0.5$')
ax.plot(t_time, rslt_2['h_time'], label=r'$A = 0.4$')
ax.legend()
ax.yaxis.get_major_ticks()[0].set_visible(False)
plt.savefig('fig-ben-porath-life-cycle-stock.png')

ax = plt.figure().add_subplot(111)
plt.xlim(0, 60)
plt.ylim(0, 100.01)
plt.xlabel(r'$t$')
plt.ylabel(r'Income')
ax.plot(t_time, rslt_1['w_time'], label=r'$A = 0.5$')
ax.plot(t_time, rslt_2['w_time'], label=r'$A = 0.4$')
ax.legend()
ax.yaxis.get_major_ticks()[0].set_visible(False)
plt.savefig('fig-ben-porath-life-cycle-income.png')
