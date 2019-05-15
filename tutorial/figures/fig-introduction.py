#!/usr/bin/env python
"""This module creates an empty canvas for the exam."""
from functools import partial

from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np


# We want to show the shape and population differences in the cost functions.
def cost_education(group, y):
    """This function calculates the cost of education."""
    if group in ['high']:
        cost = 2 / 3 * y
    else:
        cost = y
    return cost


def benefit_education(y_star, y):
    """This function calculates the benefit of education."""
    if y < y_star:
        benefit = 1.0
    else:
        benefit = 2.0
    return benefit


def unconditional_expected_marginal_product(q):
    """This function calculates the unconditional expected marginal product."""
    return 2.0 - q


def surplus_education(group, y_star, y):
    """This function calculates the surplus from education."""
    cost = cost_education(group, y)
    bene = benefit_education(y_star, y)
    return bene - cost


def align_plots(ax, ylabel, xlim=[0, 3], ylim=[0, 3], y_star=1.5):
    ax.set_xlabel('Education')
    ax.set_ylabel(ylabel)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    if y_star is not None:
        ax.axvline(y_star, color='lightgrey', linestyle='--')
        ax.text(y_star - 0.05, ylim[0] - 0.175, r'$y^*$')

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    return ax

def plots_market_structure(y_star):
    """This function plots the graphs for the analysis of the market structure."""

    for is_canvas in [False, True]:

        ax = plt.figure().add_subplot(111)
        ax.set_xlabel(r'$q_L$')
        ax.set_ylabel('Surplus')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 3])

        if not is_canvas:

            fname = 'fig-introduction-spence-market-structure.png'
            ax.set_xticks([0, 0.5, 1])

            surplus_analysis = partial(surplus_education, 'high', y_star)
            surplus_analysis = np.vectorize(surplus_analysis)
            y_values = surplus_analysis(np.tile(y_star, 1000))
            ax.plot(x_values, y_values, label='high productivity')

            surplus_analysis = partial(surplus_education, 'low', y_star)
            surplus_analysis = np.vectorize(surplus_analysis)
            y_values = surplus_analysis(np.tile(0, 1000))
            ax.plot(x_values, y_values, label='low productivity')

            y_values = unconditional_expected_marginal_product(x_values)
            ax.plot(x_values, y_values, label='no-signalling wage')
            ax.axvline(5/6, color='lightgrey', linestyle='--')

        else:

            fname = 'fig-introduction-spence-market-structure-canvas.png'
            ax.set_xticks([0, 0.5, 1])

        ax.yaxis.get_major_ticks()[0].set_visible(False)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend()

        plt.savefig(fname)


def plots_surplus(y_star):
    """This function plots the graphs for the analysis of the group surpluses."""
    for is_canvas in [True, False]:

        ax = plt.figure().add_subplot(111)

        if is_canvas:
            ax = align_plots(ax, 'Surplus', ylim=[-2, 2], y_star=None)
            fname = 'fig-introduction-spence-surplus-canvas.png'

        else:
            ax = align_plots(ax, 'Surplus', ylim=[-2, 2], y_star=y_star)
            fname = 'fig-introduction-spence-surplus.png'

            y_values = dict()
            for group in ['low', 'high']:
                surplus_analysis = partial(surplus_education, group, y_star)
                surplus_analysis = np.vectorize(surplus_analysis)

                y_values[group] = surplus_analysis(x_values)

                x_values_ma = np.ma.masked_where(
                        (x_values < y_star + 0.005) & (x_values > y_star - 0.005),
                        x_values)

                ax.plot(x_values_ma, y_values[group], label=group + ' productivity')

            ax.legend()

        plt.savefig(fname)


if __name__ == '__main__':

    x_values = np.linspace(0, 3, 1000)

    ax = plt.figure().add_subplot(111)
    ax = align_plots(ax, 'Cost', y_star=1.25)

    y_values = dict()
    linestyles = [':', '-']

    for i, group in enumerate(['low', 'high']):
        benefit_analysis = partial(cost_education, group)
        benefit_analysis = np.vectorize(benefit_analysis)

        y_values[group] = benefit_analysis(x_values)

        ax.plot(x_values, y_values[group], label=group + ' productivity', linestyle=linestyles[i])

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.legend(fontsize=25)
    plt.savefig('fig-introduction-spence-cost.png')

    ax = plt.figure().add_subplot(111)
    ax = align_plots(ax, 'Wage', y_star=1.25)

    y_star, y_values = 1.25, dict()
    benefit_analysis = partial(benefit_education, y_star)
    benefit_analysis = np.vectorize(benefit_analysis)

    y_values[group] = benefit_analysis(x_values)
    x_values_ma = np.ma.masked_where((x_values < 1.255) & (x_values > 1.2495), x_values)

    ax.plot(x_values_ma, y_values[group])

    plt.savefig('fig-introduction-spence-benefit.png')

    # This is the material for the question on market structure.
    y_star = 1.25
    plots_market_structure(y_star)

    # This is the material for the question on the surplus.
    y_star = 1.25
    plots_surplus(y_star)
