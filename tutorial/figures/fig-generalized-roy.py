#!/usr/bin/env python
"""This module creates an empty canvas for the exam."""
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np


if __name__ == '__main__':

    # This is the material for the question on the marginal benefit of treatment.
    for is_canvas in [True, False]:
        ax = plt.figure().add_subplot(111)

        ax.set_ylim(0, 0.4)
        ax.set_yticks(np.arange(0, 0.41, 0.05))

        if is_canvas:
            fname = 'fig-generalized-roy-marginal-benefit-canvas.png'
        else:
            fname = 'fig-generalized-roy-marginal-benefit.png'

            ax.set_ylabel(r"$B^{MTE}$")
            ax.set_xlabel("$u_D$")
            grid = np.linspace(0.01, 1, num=100, endpoint=True)
            alpha = np.full(100, 0.2)
            beta = alpha - 0.05 * norm.ppf(grid, loc=0.0, scale=1.0)

            ax.plot(grid, alpha, label="Presence")
            ax.plot(grid, beta, label="Absence")

        ax.yaxis.get_major_ticks()[0].set_visible(False)
        ax.set_yticklabels([])

        plt.legend()
        plt.savefig(fname)

    # This is the material for the question on the distribution of benefits and the conventional
    # average treatment effects.
    x_axis = np.arange(-2, 4, 0.001)

    for is_canvas in [True]:

        ax = plt.figure().add_subplot(111)

        plt.plot(x_axis, norm.pdf(x_axis, 1, 1))
        ax.set_xlim(-2, 4)
        ax.set_ylim(0.0, None)

        # Rename axes
        ax.set_ylabel('$f_{Y_1 - Y_0}$')
        ax.set_xlabel('$Y_1 - Y_0$')
        ax.set_yticklabels([])

        ax.legend()

        ax.yaxis.get_major_ticks()[0].set_visible(False)
        plt.tight_layout()
        plt.savefig('fig-generalized-roy-distribution-canvas.png')
